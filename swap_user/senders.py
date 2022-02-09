import logging
from abc import ABC, abstractmethod

from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class AbstractOTPSender(ABC):
    @abstractmethod
    def send(self, receiver: str, otp: str, **kwargs):
        pass

    @abstractmethod
    def render_message(self, otp: str, **kwargs):
        pass


class StdOutOTPSender(AbstractOTPSender):
    def send(self, receiver: str, otp: str, **kwargs):
        message = self.render_message(otp)
        logger.info(message)

    def render_message(self, otp: str, **kwargs):
        return f"OTP: {otp}"


class EmailOTPSender(AbstractOTPSender):
    def send(self, receiver: str, otp: str, **kwargs):
        subject = _("OTP")
        message = self.render_message(otp)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [receiver]

        send_mail(
            subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,
        )

    def render_message(self, otp: str, **kwargs):
        return f"OTP: {otp}"
