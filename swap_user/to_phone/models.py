from swap_user.to_phone.base_models import AbstractPhoneUser


class PhoneUser(AbstractPhoneUser):
    """
    Concrete implementation of user with phone login.
    """

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = "phone user"
        verbose_name_plural = "phone users"
