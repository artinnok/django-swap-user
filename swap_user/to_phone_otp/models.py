from swap_user.to_phone_otp.base_models import AbstractPhoneOTPUser


class PhoneOTPUser(AbstractPhoneOTPUser):
    """
    Concrete implementation of user with phone login.
    """

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = "OTP phone user"
        verbose_name_plural = "OTP phone users"
