from django.contrib.auth.models import (
    AbstractBaseUser as DjangoAbstractBaseUser,
    AbstractUser as DjangoAbstractUser,
    PermissionsMixin,
)
from django.db.models.options import Options
from django.db import models
from django.utils.translation import gettext_lazy as _

from swap_user.managers.email import Manager
from swap_user.settings import swap_user_settings


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

    objects = Manager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    class Meta:
        abstract = True

    def __str__(self):
        return self.email

    clean = DjangoAbstractUser.clean
    get_short_name = __str__
    get_full_name = __str__


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


class Meta:
    swappable = "AUTH_USER_MODEL"


base_classes = (swap_user_settings.EMAIL_USER_ABSTRACT_BASE_CLASS,)
EmailUser = type("EmailUser", base_classes, {
    "_meta": Options(Meta, app_label="swap_user"),
    "__module__": "swap_user.models",
    "__doc__": '\n    Point on this model if you want drop off EmailUser model with `email` field.\n    ',
})
