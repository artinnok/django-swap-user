from django.contrib.auth.base_user import AbstractBaseUser as DjangoAbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from swap_user.managers.email import EmailManager


class AbstractEmailUser(PermissionsMixin, DjangoAbstractBaseUser):
    """
    Abstract EmailUser implementation - subclass this class to provide your own
    custom User class with `email` field.

    Provides fields:
    - email
    - is_active (required by django.contrib.admin)
    - is_staff (required by django.contrib.admin)

    Provides attributes:
    - USERNAME_FIELD
    - EMAIL_FIELD
    - REQUIRED_FIELDS
    """

    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    objects = EmailManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    class Meta:
        abstract = True

    def __str__(self):
        return self.email

    clean = DjangoAbstractBaseUser.clean
    get_short_name = __str__
    get_full_name = __str__


class EmailUser(AbstractEmailUser):
    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = "email user"
        verbose_name_plural = "email users"
