from django.apps import AppConfig


class NamedEmailUserConfig(AppConfig):
    # `name` for INSTALLED_APPS
    name = "swap_user_to_named_email"
    # `verbose name` for Admin panel display
    verbose_name = "Django Swap User"
