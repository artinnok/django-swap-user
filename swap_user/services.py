from typing import Optional

from django.contrib.auth import get_user_model

from swap_user.helpers import generate_otp, get_otp_cache_key, set_otp_to_cache
from swap_user.settings import swap_user_settings


UserModel = get_user_model()


class GetOTPService:
    def generate_otp_and_send(self, username: str):
        user = self.get_user(username)
        if not user:
            return None

        user_id = user.id
        sender_class = swap_user_settings.OTP_SENDER_CLASS

        otp = generate_otp()
        cache_key = get_otp_cache_key(user_id)
        set_otp_to_cache(cache_key, otp)

        sender = sender_class()
        sender.send(username, otp)

    def get_user(self, username: str) -> Optional[str]:
        try:
            username_field = UserModel.USERNAME_FIELD
            query_data = {username_field: username}
            user = UserModel.objects.get(**query_data)
        except UserModel.DoesNotExist:
            return None

        return user
