from django.contrib.auth.base_user import AbstractBaseUser as DjangoAbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from swap_user.helpers import check_password
from swap_user.to_email_otp.managers import EmailOTPUserManager


class AbstractEmailOTPUser(PermissionsMixin):
    """
    Abstract EmailUser implementation - subclass this class to provide your own
    custom User class with `email` field.

    Main difference between this model and other models - that it doesn't
    have a `password` field.
    You need to use OTP (One Time Password) to authenticate user
    of this model and this require extra work from you on backend.

    Provides fields:
    - email
    - is_active (required by django.contrib.admin)
    - is_staff (required by django.contrib.admin)

    Provides attributes:
    - USERNAME_FIELD
    - EMAIL_FIELD

    REQUIRED_FIELDS by default will include USERNAME_FIELD and password.
    """

    email = models.EmailField(verbose_name=_("email address"), unique=True,)
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
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    objects = EmailOTPUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    # Fix `django.contrib.auth.forms.PasswordResetForm`
    EMAIL_FIELD = "email"

    class Meta:
        abstract = True

    def __str__(self):
        return self.email

    def check_password(self, user_one_time_password: str) -> bool:
        """
        Method that checks for OTP passwords match.
        """

        user_id = str(self.id)

        is_valid = check_password(user_id, user_one_time_password)

        return is_valid

    clean = DjangoAbstractBaseUser.clean
    get_username = DjangoAbstractBaseUser.get_username
    natural_key = DjangoAbstractBaseUser.natural_key
    is_anonymous = DjangoAbstractBaseUser.is_anonymous
    is_authenticated = DjangoAbstractBaseUser.is_authenticated
    get_email_field_name = DjangoAbstractBaseUser.get_email_field_name
    normalize_username = DjangoAbstractBaseUser.normalize_username

    get_short_name = __str__
    get_full_name = __str__
