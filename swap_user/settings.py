from django.conf import settings as django_settings
from django.utils.module_loading import import_string


#
# Mostly inspired by `rest_framework.settings`
#

IMPORT_SETTINGS = [
    "OTP_SENDER_CLASS",
    "GET_OTP_SERVICE_CLASS",
    "CHECK_OTP_SERVICE_CLASS",
]
DEFAULT_SETTINGS = {
    # services
    "OTP_SENDER_CLASS": "swap_user.otp.senders.StdOutOTPSender",
    "GET_OTP_SERVICE_CLASS": "swap_user.otp.services.GetOTPService",
    "CHECK_OTP_SERVICE_CLASS": "swap_user.otp.services.CheckOTPService",
    # patterns
    "INVALID_LOGIN_COUNTER_PATTERN": "swap-user:invalid:login:{user_id}",
    "SENT_OTP_COUNTER_PATTERN": "swap-user:sent:otp:{user_id}",
    "USER_BANNED_FOR_INVALID_LOGIN": "swap-user:banned:invalid:login:{user_id}",
    "USER_BANNED_FOR_OTP_RATE_LIMIT_PATTERN": "swap-user:banned:rate:limit:{user_id}",
    "OTP_PATTERN": "swap-user:otp:{user_id}",
    # constant values
    "BAN_FOR_INVALID_LOGIN_TIMEOUT": 60 * 60 * 24,  # 24 hours
    "BAN_FOR_OTP_RATE_LIMIT_TIMEOUT": 60 * 60 * 2,  # 2 hours
    "OTP_TIMEOUT": 60,  # 60 seconds
    "MAX_ATTEMPTS_OF_INVALID_LOGIN": 3,
    "MAX_NUMBER_OF_OTP_SENT": 5,
    "OTP_ALPHABET": "0123456789",
    "OTP_LENGTH": 5,
}
NAMESPACE = "SWAP_USER"

# Add default values and create working mapping
MAPPING = {
    "A": "PHONENUMBER_DB_FORMAT",
    "B": "PHONENUMBER_DEFAULT_REGION",
    "C": "PHONENUMBER_DEFAULT_FORMAT",
}


class SwapUserSettings:
    """
    Settings object mostly inspired from `rest_framework.settings`.
    """

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
