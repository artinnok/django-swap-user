from abc import ABC, abstractmethod


class AbstractOTPSender(ABC):
    """
    Abstract sender class interface.
    Subclass this and implement following methods:
        - `send`
        - `_render_message`
    """

    @abstractmethod
    def send(self, receiver: str, otp: str, **kwargs):
        """
        Put whole sending logic into this method.
        """

        pass

    @abstractmethod
    def _render_message(self, otp: str, **kwargs):
        """
        Here we can add some formatting / styling for message that you
        are going to send.
        """

        pass
