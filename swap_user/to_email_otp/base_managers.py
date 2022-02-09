from django.contrib.auth.models import BaseUserManager


class BaseEmailOTPUserManager(BaseUserManager):
    """
    Manager implementation that uses:
        - email
    """

    def create_user(self, email, **extra_fields):
        """
        Creates usual user.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create(email, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        """
        Creates super user.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create(email, **extra_fields)

    def _create(self, email, **extra_fields):
        """
        Base method that implements user creation with email and password.
        """

        if not email:
            raise ValueError("User should have email.")

        user = self.model(email=email, **extra_fields)
        user.save()

        return user
