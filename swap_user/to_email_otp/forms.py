from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


UserModel = get_user_model()


class GetOTPForm(forms.Form):
    email = forms.EmailField(label=_("Email"))


class CheckOTPForm(forms.Form):
    password = forms.CharField(label=_("OTP"), widget=forms.PasswordInput)
