from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from swap_user.helpers import (
    check_user_was_banned,
    get_banned_for_invalid_login_cache_key,
    get_banned_for_otp_rate_limit_cache_key,
    normalize_username,
)


UserModel = get_user_model()


class GetOTPForm(forms.ModelForm):
    """
    Unfortunately we can't check User exist or not at this screen by the
    security reasons - if we will show error when User doesn't exist,
    attacker can just check all the emails / phones.
    """

    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD,)

    def clean(self):
        """
        We are preventing unique validation by overriding this method and
        adding extra check for user ban.
        """

        username_field = UserModel.USERNAME_FIELD
        raw_username = self.cleaned_data[username_field]
        username = normalize_username(raw_username)

        self._check_user_is_banned_for_otp_rate_limit(username)
        self._check_user_is_banned_for_invalid_login_attempts(username)

        return self.cleaned_data

    def _check_user_is_banned_for_otp_rate_limit(self, username: str):
        """
        We are banning user for too many sent OTP codes.
        Here is a check.
        """

        cache_key = get_banned_for_otp_rate_limit_cache_key(username)
        is_banned = check_user_was_banned(cache_key)

        if is_banned:
            message = _("You are banned - try again later.")
            code = "banned"
            raise forms.ValidationError(message, code)

    def _check_user_is_banned_for_invalid_login_attempts(self, username: str):
        """
        We are banning user for too many invalid login
        attempts.
        Here we are checking for this.
        """

        cache_key = get_banned_for_invalid_login_cache_key(username)
        is_banned = check_user_was_banned(cache_key)

        if is_banned:
            message = _("You are banned - contact with admin.")
            code = "banned"
            raise forms.ValidationError(message, code)


class CheckOTPForm(GetOTPForm):
    """
    Here we are checking User presence among with OPT check.
    """

    otp = forms.CharField(label=_("OTP"), widget=forms.PasswordInput(attrs={"autofocus": True}))

    def clean(self):
        """
        Method that allows to us pass through few validation checks:
            - User DB presence
            - OTP password validity
        """

        username_field = UserModel.USERNAME_FIELD
        username = self.cleaned_data[username_field]
        otp = self.cleaned_data["otp"]

        self._check_user_is_banned_for_invalid_login_attempts(username)
        user = self._get_user(username)
        self._check_password(user, otp)

    def _get_user(self, username: str) -> UserModel:
        """
        Check User presence in our DB or not.
        """

        username_field = UserModel.USERNAME_FIELD
        query_data = {username_field: username}

        try:
            user = UserModel.objects.get(**query_data)
        except UserModel.DoesNotExist:
            message = _("Invalid credentials.")
            code = "invalid_credentials"
            raise forms.ValidationError(message, code)

        return user

    def _check_password(self, user: UserModel, otp: str):
        """
        Check backend cached OTP with user provided OTP.
        """

        if not user.check_password(otp):
            message = _("Invalid credentials.")
            code = "invalid_credentials"
            raise forms.ValidationError(message, code)
