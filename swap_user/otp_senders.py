import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from swap_user.base_senders import AbstractOTPSender


logger = logging.getLogger(__name__)


class StdOutOTPSender(AbstractOTPSender):
    def send(self, receiver: str, otp: str, **kwargs):
        message = self._render_message(otp)
        logger.info(message)

    def _render_message(self, otp: str, **kwargs):
        return f"OTP: {otp}"


class EmailOTPSender(AbstractOTPSender):
    def send(self, receiver: str, otp: str, **kwargs):
        subject = _("OTP")
        message = self._render_message(otp)
        from_email = self._get_from_email()
        recipient_list = [receiver]

        send_mail(
            subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,
        )

    def _render_message(self, otp: str, **kwargs):
        return f"OTP: {otp}"

    def _get_from_email(self):
        return settings.EMAIL_HOST_USER
