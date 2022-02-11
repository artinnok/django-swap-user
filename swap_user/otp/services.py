from typing import Optional

from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpRequest

from swap_user.helpers import generate_otp, get_otp_cache_key, set_otp_to_cache
from swap_user.settings import swap_user_settings


UserModel = get_user_model()


class GetOTPService:
    def generate_otp_and_send(self, username: str):
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
        set_otp_to_cache(cache_key, otp)

        sender = sender_class()
        sender.send(username, otp)

    def _get_user(self, username: str) -> Optional[UserModel]:
        username_field = UserModel.USERNAME_FIELD
        query_data = {username_field: username}

        try:
            user = UserModel.objects.get(**query_data)
        except UserModel.DoesNotExist:
            return None

        return user

    def _has_enough_permissions(self, user: UserModel) -> bool:
        is_staff = user.is_staff
        is_active = user.is_active

        return is_staff and is_active


class CheckOTPService:
    def authenticate_and_login(self, request: HttpRequest, username: str, password: str):
        user = authenticate(request, username=username, password=password,)
        login(request, user)
