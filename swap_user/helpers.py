import secrets

from django.core.cache import cache

from swap_user.settings import swap_user_settings


def generate_otp() -> str:
    """
    Method that generates OTP (One Time Password).
    """

    otp_alphabet = swap_user_settings.OTP_ALPHABET
    otp_length = swap_user_settings.OTP_LENGTH

    otp_digits = [secrets.choice(otp_alphabet) for _ in range(otp_length)]
    otp = "".join(otp_digits)

    return otp


def set_otp_to_cache(otp_key: str, otp_value: str, expire=swap_user_settings.OTP_TIMEOUT) -> str:
    """
    Saves OTP (One Time Password) into cache with provided key.
    """

    cache.set(otp_key, otp_value, expire)

    return otp_value


def get_otp_cache_key(user_id: str) -> str:
    """
    Generates cache key for storing OTP (One Time Password) per user.
    """

    cache_key = swap_user_settings.OTP_PATTERN.format(user_id=user_id)

    return cache_key


def check_password(user_id: str, user_one_time_password: str) -> bool:
    """
    Method that checks for OTP passwords match.
    """

    cache_key = get_otp_cache_key(user_id)
    backend_one_time_password = cache.get(cache_key)

    is_same_password = backend_one_time_password == user_one_time_password

    return is_same_password
