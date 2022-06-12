from swap_user.to_email.base_models import AbstractEmailUser


class EmailUser(AbstractEmailUser):
    """
    Concrete implementation of user with email login without OTP.
    """

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = "email user"
        verbose_name_plural = "email users"
