from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


UserModel = get_user_model()


class GetOTPForm(forms.Form):
    """
    Unfortunately we can't check User exist or not by the
    security reasons - if we will show error when User doesn't exist,
    attacker can just check all the emails.

    # TODO add admin check
    """

    email = forms.EmailField(label=_("Email"))


class CheckOTPForm(GetOTPForm):
    otp = forms.CharField(label=_("OTP"), widget=forms.PasswordInput)
