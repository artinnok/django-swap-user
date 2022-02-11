from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.views import REDIRECT_FIELD_NAME, LoginView, SuccessURLAllowedHostsMixin
from django.views.generic.edit import FormView

from swap_user.settings import swap_user_settings
from swap_user.to_email_otp.otp_forms import CheckOTPForm, GetOTPForm


UserModel = get_user_model()


class GetOTPView(FormView):
    """
    This view helps to send OTP via `OTPSender` subclasses
    """

    template_name = "admin/login-otp.html"
    form_class = GetOTPForm
    success_url = "/admin/check-otp/?next=/admin/"

    def form_valid(self, form: forms.Form):
        username = form.cleaned_data["username"]

        service_class = swap_user_settings.GET_OTP_SERVICE_CLASS
        service = service_class()
        service.generate_otp_and_send(username=username)

        return super().form_valid(form)


class CheckOTPView(SuccessURLAllowedHostsMixin, FormView):
    """
    We are validating OTP that comes from user.
    """

    template_name = "admin/check-otp.html"
    form_class = CheckOTPForm
    redirect_field_name = REDIRECT_FIELD_NAME

    def form_valid(self, form: forms.Form):
        username_field = UserModel.USERNAME_FIELD
        username = form.cleaned_data[username_field]
        otp_password = form.cleaned_data["otp"]

        service_class = swap_user_settings.CHECK_OTP_SERVICE_CLASS
        service = service_class()
        service.authenticate_and_login(
            request=self.request, username=username, password=otp_password,
        )

        return super().form_valid(form)

    get_success_url = LoginView.get_success_url
    get_redirect_url = LoginView.get_redirect_url
