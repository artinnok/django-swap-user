from django.core.cache import cache

from swap_user.to_email_otp.helpers import get_otp_cache_key
from swap_user.to_email_otp.models import EmailOTPUser


class EmailOTPAuthBackend:
    def authenticate(self, request, email: str, otp_from_user: str, **credentials):
        """
        Authenticates used based on OTP (One Time Password) because current user model
        doesn't have a `password` field.

        Reference - https://docs.djangoproject.com/en/dev/topics/auth/customizing/#writing-an-authentication-backend
        """

        try:
            user = EmailOTPUser.objects.get(email=email)
            user_id = user.id

            cache_key = get_otp_cache_key(user_id)
            otp_value_from_cache = cache.get(cache_key)

            if otp_value_from_cache != otp_from_user:
                return None

            return user
        except EmailOTPUser.DoesNotExist:
            return None

    def get_user(self, user_id: int):
        """
        Returns user instance based on PK or None.

        Reference - https://docs.djangoproject.com/en/dev/topics/auth/customizing/#writing-an-authentication-backend
        """

        try:
            user = EmailOTPUser.objects.get(pk=user_id)

            return user
        except EmailOTPUser.DoesNotExist:
            return None
