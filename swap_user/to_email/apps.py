from django.apps import AppConfig


class EmailUserConfig(AppConfig):
    # `name` for INSTALLED_APPS
    name = "swap_user.to_email"
    # `label` used for relations reference in format `app_label.Model`
    # also it used for `AUTH_USER_MODEL` settings and fixtures definition
    label = "swap_to_email"
    # `verbose name` for Admin panel display
    verbose_name = "Django Swap User"
    # we are maintaining historical behavior
    default_auto_field = "django.db.models.AutoField"
