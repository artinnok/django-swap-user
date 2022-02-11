import secrets
from typing import Union

from django.core.cache import cache

from swap_user.settings import swap_user_settings


DEFAULT_COUNTER_VALUE = 1
DEFAULT_BANNED_VALUE = False


def generate_otp() -> str:
    """
    Method that generates OTP (One Time Password).
    """

    otp_alphabet = swap_user_settings.OTP_ALPHABET
    otp_length = swap_user_settings.OTP_LENGTH

    otp_digits = [secrets.choice(otp_alphabet) for _ in range(otp_length)]
    otp = "".join(otp_digits)

    return otp


def set_key_to_cache(
    cache_key: str, value: Union[int, str], expire=swap_user_settings.OTP_TIMEOUT
) -> str:
    """
    Saves value into cache with provided key.
    """

    cache.set(cache_key, value, expire)

    return value


def get_otp_cache_key(user_id: str) -> str:
    """
    Generates cache key for storing OTP (One Time Password) per user.
    """

    cache_key = swap_user_settings.OTP_PATTERN.format(user_id=user_id)

    return cache_key


def get_invalid_login_cache_key(user_id: str) -> str:
    """
    Get invalid login cache key for concrete user.
    """

    cache_key = swap_user_settings.INVALID_LOGIN_PATTERN.format(user_id=user_id)

    return cache_key


def get_banned_user_cache_key(user_id: str) -> str:
    """
    Get banned user cache key
    """

    cache_key = swap_user_settings.BANNED_USER_PATTERN.format(user_id=user_id)

    return cache_key


def increase_counter_of_invalid_login(cache_key: str) -> int:
    """
    Increase counter of invalid login by 1.
    """

    try:
        current_counter = cache.incr(cache_key)
    except ValueError:
        current_counter = cache.set(cache_key, DEFAULT_COUNTER_VALUE)

    return current_counter


def check_password(user_id: str, user_one_time_password: str) -> bool:
    """
    Function that checks for OTP passwords match.
    """

    cache_key = get_otp_cache_key(user_id)
    backend_one_time_password = cache.get(cache_key)

    is_same_password = backend_one_time_password == user_one_time_password

    return is_same_password


def check_user_was_banned(cache_key: str) -> bool:
    """
    Checks user is banned or not.
    """

    is_banned = cache.get(cache_key, DEFAULT_BANNED_VALUE)

    return is_banned
