from typing import Optional

from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpRequest

from swap_user.helpers import (
    generate_otp,
    get_banned_user_cache_key,
    get_invalid_login_cache_key,
    get_otp_cache_key,
    increase_counter_of_invalid_login,
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

        otp = generate_otp()
        cache_key = get_otp_cache_key(user_id)
        set_key_to_cache(cache_key=cache_key, value=otp)

        sender = sender_class()
        sender.send(username, otp)

    def save_username_to_sesson(self, request: HttpRequest, username: str):
        """
        Save username to session for future usage at the next
        screen (view `CheckOTPView`). Just convenient for future steps.
        """

        request.session[UserModel.USERNAME_FIELD] = username

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

    def track_invalid_login_attempt(self, username: str):
        """
        Here we are going to track all invalid login attempts.
        When invalid attempts will reach a limit - user will be banned for some period.
        """

        invalid_login_cache_key = get_invalid_login_cache_key(username)
        current_counter = increase_counter_of_invalid_login(invalid_login_cache_key)

        if current_counter < swap_user_settings.MAX_INVALID_LOGIN_ATTEMPTS:
            return None

        banned_user_cache_key = get_banned_user_cache_key(username)
        set_key_to_cache(
            cache_key=banned_user_cache_key,
            value=USER_IS_BANNED,
            expire=swap_user_settings.BANNED_USER_TIMEOUT,
        )
