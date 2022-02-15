from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.views import REDIRECT_FIELD_NAME, LoginView, SuccessURLAllowedHostsMixin
from django.views.generic.edit import FormView

from swap_user.helpers import normalize_username
from swap_user.otp.forms import CheckOTPForm, GetOTPForm
from swap_user.settings import swap_user_settings


UserModel = get_user_model()


class GetOTPView(FormView):
    """
    This view helps to send OTP via `OTPSender` subclasses
    """

    template_name = "admin/login-otp.html"
    form_class = GetOTPForm
    success_url = "/admin/check-otp/?next=/admin/"

    def form_valid(self, form: forms.Form):
        """
        If form is valid, we will use corresponding service and do the following:
            - Generate OTP and send it
            - Save username for autofill on the next screen
        """

        username_field = UserModel.USERNAME_FIELD
        raw_username = form.cleaned_data[username_field]
        username = normalize_username(raw_username)
        request = self.request

        service_class = swap_user_settings.GET_OTP_SERVICE_CLASS
        service = service_class()

        service.generate_otp_and_send(username=username)
        service.save_username_to_sesson(request=request, username=username)
        service.track_how_much_otp_sent(username=username)

        return super().form_valid(form)


class CheckOTPView(SuccessURLAllowedHostsMixin, FormView):
    """
    We are validating OTP that comes from user.
    """

    template_name = "admin/check-otp.html"
    form_class = CheckOTPForm
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_initial(self):
        """
        Let's try to autofill username at the next screen after OTP was sent.
        Convenient for human - no need to provide email one more time.
        """

        session = self.request.session
        cached_username = session.get(UserModel.USERNAME_FIELD, "")
        username_field = UserModel.USERNAME_FIELD

        initial = {username_field: cached_username}

        return initial

    def form_valid(self, form: forms.Form):
        """
        If form is valid - we will do:
            - Authenticate
            - Login
        """

        username_field = UserModel.USERNAME_FIELD
        raw_username = form.cleaned_data[username_field]
        username = normalize_username(raw_username)
        otp_password = form.cleaned_data["otp"]

        service_class = swap_user_settings.CHECK_OTP_SERVICE_CLASS
        service = service_class()
        service.authenticate_and_login(
            request=self.request, username=username, password=otp_password,
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        If form is invalid - we will increase counter of invalid logins for current user.
        When counter will reach the limit - user will be banned for some amount of time.
        """

        username_field = UserModel.USERNAME_FIELD
        raw_username = form.cleaned_data[username_field]
        username = normalize_username(raw_username)

        service_class = swap_user_settings.CHECK_OTP_SERVICE_CLASS
        service = service_class()
        service.track_invalid_login_attempt(username=username)

        return super().form_invalid(form)

    get_success_url = LoginView.get_success_url
    get_redirect_url = LoginView.get_redirect_url
