from django.core.cache import cache

from swap_user.to_phone_otp.helpers import generate_otp_cache_key
from swap_user.to_phone_otp.models import PhoneOTPUser


class PhoneOTPAuthBackend:
    def authenticate(self, request, phone: str, otp_from_user: str, **credentials):
        """
        Authenticates used based on OTP (One Time Password) because current user model
        doesn't have a `password` field.

        Reference - Reference - https://docs.djangoproject.com/en/dev/topics/auth/customizing/#writing-an-authentication-backend
        """

        try:
            user = PhoneOTPUser.objects.get(phone=phone)
            user_id = user.id

            cache_key = generate_otp_cache_key(user_id)
            otp_value_from_cache = cache.get(cache_key)

            if otp_value_from_cache != otp_from_user:
                return None

            return user
        except PhoneOTPUser.DoesNotExist:
            return None

    def get_user(self, user_id: int):
        """
        Returns user instance based on PK or None.

        Reference - https://docs.djangoproject.com/en/dev/topics/auth/customizing/#writing-an-authentication-backend
        """

        try:
            return PhoneOTPUser.objects.get(pk=user_id)
        except PhoneOTPUser.DoesNotExist:
            return None
