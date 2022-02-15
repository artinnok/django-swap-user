from typing import Optional

from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpRequest

from swap_user.helpers import (
    generate_otp,
    get_banned_for_invalid_login_cache_key,
    get_banned_for_otp_rate_limit_cache_key,
    get_invalid_login_counter_cache_key,
    get_otp_cache_key,
    get_sent_otp_counter_cache_key,
    increase_counter,
    set_key_to_cache,
)
from swap_user.settings import swap_user_settings


UserModel = get_user_model()
USER_IS_BANNED = True


class GetOTPService:
    """
    Service for `GetOTPView`, that handles whole logic of sending OTP
    code such as:
        - Decides we can send OTP to this User or not
        - Generates and caches OTP
        - Sends OTP to User
    """

    def generate_otp_and_send(self, username: str):
        """
        Main handler of service, which holds all logical steps.
        """

        user = self._get_user(username)
        if not user:
            return None

        is_enough_permissions = self._has_enough_permissions(user)
        if not is_enough_permissions:
            return None

        user_id = user.id
        sender_class = swap_user_settings.OTP_SENDER_CLASS

        otp = self._generate_and_cache_otp(user_id)

        sender = sender_class()
        sender.send(username, otp)

    def save_username_to_sesson(self, request: HttpRequest, username: str):
        """
        Save username to session for future usage at the next
        screen (view `CheckOTPView`). Just convenient for future steps.
        """

        request.session[UserModel.USERNAME_FIELD] = username

    def track_how_much_otp_sent(
        self,
        username: str,
        max_number_of_otp: int = swap_user_settings.MAX_NUMBER_OF_OTP_SENT,
        ban_timeout: int = swap_user_settings.BAN_FOR_OTP_RATE_LIMIT_TIMEOUT,
    ):
        """
        We are tracking how much OTP we are sending to user.
        If user reached limit of sent OTP number - he is going to ban.
        """

        sent_otp_cache_key = get_sent_otp_counter_cache_key(username)

        current_counter = increase_counter(sent_otp_cache_key)

        if current_counter < max_number_of_otp:
            return None

        rate_limit_cache_key = get_banned_for_otp_rate_limit_cache_key(username)
        set_key_to_cache(
            cache_key=rate_limit_cache_key, value=USER_IS_BANNED, expire=ban_timeout,
        )

    def _get_user(self, username: str) -> Optional[UserModel]:
        """
        Method, that handles user presence in our DB or not.
        """

        username_field = UserModel.USERNAME_FIELD
        query_data = {username_field: username}

        try:
            user = UserModel.objects.get(**query_data)
        except UserModel.DoesNotExist:
            return None

        return user

    def _has_enough_permissions(self, user: UserModel) -> bool:
        """
        Override this, if you need to customize conditions when email
        will be sent to user.
        """

        is_staff = user.is_staff
        is_active = user.is_active

        return is_staff and is_active

    def _generate_and_cache_otp(self, user_id: str) -> str:
        """
        Generates OTP and writes it into cache.
        """

        otp = generate_otp()
        cache_key = get_otp_cache_key(user_id)
        set_key_to_cache(cache_key=cache_key, value=otp)

        return otp


class CheckOTPService:
    """
    Service for `CheckOTPView` which authenticates (or not) and then
    we are proceeding through default Django's login process - i.e. writing
    to session and cookies.
    """

    def authenticate_and_login(self, request: HttpRequest, username: str, password: str):
        """
        Default authentication and login process to enter Django's admin.
        """

        user = authenticate(request, username=username, password=password,)
        login(request, user)

    def track_invalid_login_attempt(
        self,
        username: str,
        max_invalid_attempts: int = swap_user_settings.MAX_ATTEMPTS_OF_INVALID_LOGIN,
        ban_timeout: int = swap_user_settings.BAN_FOR_INVALID_LOGIN_TIMEOUT,
    ):
        """
        Here we are going to track all invalid login attempts.
        When invalid attempts will reach a limit - user will be banned for some period.
        """

        invalid_login_cache_key = get_invalid_login_counter_cache_key(username)
        current_counter = increase_counter(invalid_login_cache_key)

        if current_counter < max_invalid_attempts:
            return None

        banned_user_cache_key = get_banned_for_invalid_login_cache_key(username)
        set_key_to_cache(
            cache_key=banned_user_cache_key, value=USER_IS_BANNED, expire=ban_timeout,
        )
