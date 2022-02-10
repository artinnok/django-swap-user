from abc import ABC, abstractmethod


class AbstractOTPSender(ABC):
    @abstractmethod
    def send(self, receiver: str, otp: str, **kwargs):
        pass

    @abstractmethod
    def _render_message(self, otp: str, **kwargs):
        pass
