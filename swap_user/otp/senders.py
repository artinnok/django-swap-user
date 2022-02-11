import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from swap_user.base_senders import AbstractOTPSender


logger = logging.getLogger(__name__)


class StdOutOTPSender(AbstractOTPSender):
    """
    Simple sender that just writes all messages to STDOUT.
    """

    def send(self, receiver: str, otp: str, **kwargs):
        """
        Writes OTP message to STDOUT.
        """

        message = self._render_message(otp)
        logger.info(message)

    def _render_message(self, otp: str, **kwargs):
        return f"OTP: {otp}"


class EmailOTPSender(AbstractOTPSender):
    """
    Sender that implements sending OTP via default `send_mail`
    function. To make this work you need to set following settings:
        - `EMAIL_HOST`
        - `EMAIL_HOST_PASSWORD`
        - `EMAIL_HOST_USER`
        - `EMAIL_PORT`
        - `EMAIL_USE_TLS`
        - `EMAIL_USE_SSL`
    """

    def send(self, receiver: str, otp: str, **kwargs):
        """
        Sends OTP via email.
        """

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
        """
        Override this, if your settings are differs from this.
        """

        return settings.EMAIL_HOST_USER
