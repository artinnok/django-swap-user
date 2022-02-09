from django.contrib.auth.base_user import BaseUserManager


class BasePhoneOTPUserManager(BaseUserManager):
    """
    Manager implementation that uses:
        - phone
    """

    def create_user(self, phone, **extra_fields):
        """
        Creates usual user.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create(phone, **extra_fields)

    def create_superuser(self, phone, **extra_fields):
        """
        Creates super user.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create(phone, **extra_fields)

    def _create(self, phone, **extra_fields):
        """
        Base method that implements user creation with email and password.
        """

        if not phone:
            raise ValueError("User should have phone number.")

        user = self.model(phone=phone, **extra_fields)
        user.save()

        return user
