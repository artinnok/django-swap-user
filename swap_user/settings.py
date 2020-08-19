from django.conf import settings
from django.utils.module_loading import import_string


IMPORT_SETTINGS = [
    "EMAIL_USER_ABSTRACT_BASE_CLASS",
]


class SwapUserSettings:
    EMAIL_USER_ABSTRACT_BASE_CLASS = "swap_user.models.email.AbstractEmailUser"

    def __init__(self):
        for key, value in self.__dict__.items():
            if key not in IMPORT_SETTINGS:
                continue

            module = import_string(value)
            setattr(self, key, module)

    def __getattr__(self, item):
        try:
            getattr(settings, item)
        except AttributeError:
            return getattr(self, item)


swap_user_settings = SwapUserSettings()
