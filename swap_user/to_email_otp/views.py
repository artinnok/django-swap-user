from django.views.generic.edit import FormView

from swap_user.to_email_otp.forms import CheckOTPForm, GetOTPForm
from swap_user.to_email_otp.services import OTPSender


class GetOTPView(FormView):
    """
    This view helps to send OTP via `OTPSender` subclasses
    """

    template_name = "admin/otp-login.html"
    form_class = GetOTPForm
    success_url = "/admin/otp-check/"

    def form_valid(self, form):
        sender = OTPSender()
        sender.send()
        return super(GetOTPView, self).form_valid(form)


class CheckOTPView(FormView):
    """
    We are validating OTP that comes from user.
    """

    template_name = "admin/otp-check.html"
    form_class = CheckOTPForm
    success_url = "/admin/"
