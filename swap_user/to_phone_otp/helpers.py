import secrets

from swap_user.settings import swap_user_settings


def generate_otp():
    """
    Private method that generates OTP (One Time Password).
    """

    otp_alphabet = swap_user_settings.OTP_ALPHABET
    otp_length = swap_user_settings.OTP_LENGTH

    otp_digits = [secrets.choice(otp_alphabet) for _ in range(otp_length)]
    otp = "".join(otp_digits)

    return otp


def generate_otp_cache_key(user_id):
    """
    Generates cache key for storing OTP (One Time Password) per user.
    """

    cache_key = swap_user_settings.OTP_PATTERN.format(user_id=user_id)

    return cache_key
