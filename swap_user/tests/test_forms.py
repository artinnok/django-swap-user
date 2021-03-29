from unittest.mock import MagicMock

from swap_user.to_named_email.forms import NamedUserEmailOptionalFieldsForm


def test_save_field():
    instance = MagicMock()
    data = {
        "email": "hello@world.com",
        "first_name": "Hello",
        "last_name": "World",
    }
    form = NamedUserEmailOptionalFieldsForm(data=data, instance=instance)

    assert form.is_valid() is True


def test_one_password():
    instance = MagicMock()
    data = {
        "email": "hello@world.com",
        "password_1": "Hello",
    }
    form = NamedUserEmailOptionalFieldsForm(data=data, instance=instance)

    assert form.is_valid() is False
    assert (
        form.errors.as_json()
        == '{"__all__": [{"message": "Provide both of passwords", "code": "provide_both_passwords"}]}'
    )


def test_not_matching_passwords():
    instance = MagicMock()
    data = {
        "email": "hello@world.com",
        "password_1": "Hello",
        "password_2": "World",
    }
    form = NamedUserEmailOptionalFieldsForm(data=data, instance=instance)

    assert form.is_valid() is False
    assert (
        form.errors.as_json()
        == '{"__all__": [{"message": "Passwords should be same", "code": "password_should_be_same"}]}'
    )


def test_matching_passwords():
    instance = MagicMock()
    data = {
        "email": "hello@world.com",
        "password_1": "Hello",
        "password_2": "Hello",
    }
    form = NamedUserEmailOptionalFieldsForm(data=data, instance=instance)

    assert form.is_valid() is True
