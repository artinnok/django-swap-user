import logging
from abc import ABC, abstractmethod


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
