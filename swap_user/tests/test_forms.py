from unittest.mock import MagicMock

from swap_user.named_email.forms import NamedUserEmailForm


def test_empty_password():
    instance = MagicMock()
    data = {"first_name": "Hello", "last_name": "World"}
    form = NamedUserEmailForm(data=data, instance=instance)

    assert form.is_valid() == False
