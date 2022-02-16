from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from swap_user.helpers import normalize_username
from swap_user.settings import swap_user_settings


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

        service_class = swap_user_settings.VALIDATION_SERVICE_CLASS
        service = service_class()

        service.check_user_is_banned_for_otp_rate_limit(username)
        service.check_user_is_banned_for_invalid_login_attempts(username)
        service.check_extra(username=username)

        return self.cleaned_data


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

        service_class = swap_user_settings.VALIDATION_SERVICE_CLASS
        service = service_class()

        service.check_user_is_banned_for_invalid_login_attempts(username)
        service.check_password(username, otp)
        service.check_extra(username=username, otp=otp)

        return self.cleaned_data
