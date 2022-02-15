import secrets
from typing import Union

from django.core.cache import cache

from swap_user.settings import swap_user_settings


DEFAULT_COUNTER_VALUE = 1
DEFAULT_BANNED_VALUE = False


def generate_otp(
    alphabet: str = swap_user_settings.OTP_ALPHABET, length: int = swap_user_settings.OTP_LENGTH
) -> str:
    """
    Method that generates OTP (One Time Password).
    """

    otp_digits = [secrets.choice(alphabet) for _ in range(length)]
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


def get_otp_cache_key(user_id: str, cache_pattern: str = swap_user_settings.OTP_PATTERN) -> str:
    """
    Generates cache key for storing OTP (One Time Password) per user.
    """

    cache_key = cache_pattern.format(user_id=user_id)

    return cache_key


def get_banned_for_invalid_login_cache_key(
    user_id: str, cache_pattern: str = swap_user_settings.USER_BANNED_FOR_INVALID_LOGIN
) -> str:
    """
    Get banned user cache key.
    """

    cache_key = cache_pattern.format(user_id=user_id)

    return cache_key


def get_banned_for_otp_rate_limit_cache_key(
    user_id: str, cache_pattern: str = swap_user_settings.USER_BANNED_FOR_OTP_RATE_LIMIT_PATTERN
) -> str:
    """
    Get banned for too many sent OTP pattern.
    """

    cache_key = cache_pattern.format(user_id=user_id)

    return cache_key


def get_invalid_login_counter_cache_key(
    user_id: str, cache_pattern: str = swap_user_settings.INVALID_LOGIN_COUNTER_PATTERN
) -> str:
    """
    Get invalid login cache key for concrete user.
    """

    cache_key = cache_pattern.format(user_id=user_id)

    return cache_key


def get_sent_otp_counter_cache_key(
    user_id: str, cache_pattern: str = swap_user_settings.SENT_OTP_COUNTER_PATTERN
) -> str:
    """
    Get how much OTP sent to concrete user.
    """

    cache_key = cache_pattern.format(user_id=user_id)

    return cache_key


def increase_counter(cache_key: str, default_counter_value: int = DEFAULT_COUNTER_VALUE) -> int:
    """
    Increase counter of invalid login by 1.
    """

    try:
        current_counter = cache.incr(cache_key)
    except ValueError:
        current_counter = cache.set(cache_key, default_counter_value)

    return current_counter


def check_password(user_id: str, user_one_time_password: str) -> bool:
    """
    Function that checks for OTP passwords match.
    """

    cache_key = get_otp_cache_key(user_id)
    backend_one_time_password = cache.get(cache_key)

    is_same_password = backend_one_time_password == user_one_time_password

    return is_same_password


def check_user_was_banned(cache_key: str, default_ban_value: bool = DEFAULT_BANNED_VALUE) -> bool:
    """
    Checks user is banned or not.
    """

    is_banned = cache.get(cache_key, default_ban_value)

    return is_banned


def normalize_username(username: str) -> str:
    """
    Username normalization function:
        - Removes all spaces
        - Transforms to lowercase
    """

    normalized = username.strip().lower()

    return normalized
