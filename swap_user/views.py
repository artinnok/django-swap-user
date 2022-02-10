from django.contrib.auth import get_user_model, authenticate
from django.views.generic.edit import FormView
from django import forms

from swap_user.services import GetOTPService
from swap_user.to_email_otp.forms import CheckOTPForm, GetOTPForm


UserModel = get_user_model()


class GetOTPView(FormView):
    """
    This view helps to send OTP via `OTPSender` subclasses
    """

    template_name = "admin/login-otp.html"
    form_class = GetOTPForm
    success_url = "/admin/check-otp/"

    def form_valid(self, form: forms.Form):
        username_field = UserModel.USERNAME_FIELD
        username = form.cleaned_data[username_field]

        service = GetOTPService()
        service.generate_otp_and_send(username)

        return super().form_valid(form)


class CheckOTPView(FormView):
    """
    We are validating OTP that comes from user.
    """

    template_name = "admin/check-otp.html"
    form_class = CheckOTPForm
    success_url = "/admin/"

    def form_valid(self, form: forms.Form):
        username_field = UserModel.USERNAME_FIELD
        username = form.cleaned_data[username_field]
        otp_password = form.cleaned_data["otp"]

        authenticate(self.request, password=otp_password, username=username)

        return super().form_valid(form)
