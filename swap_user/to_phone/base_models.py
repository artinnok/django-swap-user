from django.contrib.auth.base_user import AbstractBaseUser as DjangoAbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from swap_user.to_phone.managers import PhoneUserManager


class AbstractPhoneUser(PermissionsMixin, DjangoAbstractBaseUser):
    """
    Abstract PhoneUser implementation - subclass this class to provide your own
    custom User class with `phone` field.

    Provides fields:
    - phone
    - is_active (required by django.contrib.admin)
    - is_staff (required by django.contrib.admin)

    Provides attributes:
    - USERNAME_FIELD
    - EMAIL_FIELD

    REQUIRED_FIELDS by default will include USERNAME_FIELD and password.
    """

    phone = PhoneNumberField(verbose_name=_("phone number"), unique=True,)
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

    objects = PhoneUserManager()

    USERNAME_FIELD = "phone"
    # Fix `django.contrib.auth.forms.PasswordResetForm`
    EMAIL_FIELD = "email"

    class Meta:
        abstract = True

    def __str__(self):
        return self.phone.as_e164

    clean = DjangoAbstractBaseUser.clean

    get_short_name = __str__
    get_full_name = __str__
