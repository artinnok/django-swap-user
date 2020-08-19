from django.conf import settings as django_settings
from django.utils.module_loading import import_string

IMPORT_SETTINGS = [
    "EMAIL_USER_ABSTRACT_BASE_CLASS",
]
DEFAULT_SETTINGS = {"EMAIL_USER_ABSTRACT_BASE_CLASS": "swap_user.email.models.AbstractEmailUser"}
NAMESPACE = "SWAP_USER"


class SwapUserSettings:
    def make_import(self, item, path):
        val = import_string(path)
        setattr(self, item, val)

        return val

    def __getattr__(self, item):
        try:
            namespaced_settings = getattr(django_settings, NAMESPACE)
            value = namespaced_settings[item]
        except (AttributeError, KeyError):
            value = DEFAULT_SETTINGS[item]

        if item in IMPORT_SETTINGS:
            value = self.make_import(item, value)

        return value


swap_user_settings = SwapUserSettings()
