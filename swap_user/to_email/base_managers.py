from django.contrib.auth.models import BaseUserManager


class BaseEmailUserManager(BaseUserManager):
    """
    Manager implementation that uses:
        - email
        - password
    """

    def create_user(self, email, password, **extra_fields):
        """
        Creates usual user.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates super user.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create(email, password, **extra_fields)

    def _create(self, email, password, **extra_fields):
        """
        Base method that implements user creation with email and password.
        """

        if not email:
            raise ValueError("User should have email.")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user
