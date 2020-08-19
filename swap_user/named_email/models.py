from django.db import models
from django.utils.translation import gettext_lazy as _

from swap_user.email.models import AbstractEmailUser


class AbstractNamedEmailUser(AbstractEmailUser):
    """
    Use this abstract class if you want to add a user with
    first name and last name.
    """

    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=50,
        # maybe remove
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=100,
        # maybe remove
        blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class NamedEmailUser(AbstractNamedEmailUser):
    class Meta:
        swappable = "AUTH_USER_MODEL"
