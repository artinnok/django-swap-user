from swap_user.to_email.base_models import AbstractEmailUser


class EmailUser(AbstractEmailUser):
    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = "email user"
        verbose_name_plural = "email users"
