from django.apps import AppConfig


class EmailUserConfig(AppConfig):
    # `name` for INSTALLED_APPS
    name = "swap_user.to_email"
    # `verbose name` for Admin panel display
    verbose_name = "Django Swap User"
