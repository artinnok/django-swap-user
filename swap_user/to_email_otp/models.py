from swap_user.to_email_otp.base_models import AbstractEmailOTPUser


class EmailOTPUser(AbstractEmailOTPUser):
    """
    Concrete implementation of user with email login.
    """

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = "OTP email user"
        verbose_name_plural = "OTP email users"
