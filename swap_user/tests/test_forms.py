from unittest.mock import MagicMock

from swap_user.to_email.forms import EmailUserOptionalFieldsForm


def test_save_field():
    """
    Test whether user fields within the form are being valid and accepted.
    """

    instance = MagicMock()
    data = {
        "email": "hello@world.com",
        "first_name": "Hello",
        "last_name": "World",
    }
    form = EmailUserOptionalFieldsForm(data=data, instance=instance)

    assert form.is_valid() is True


def test_one_password():
    """
    Test whether both password fields within the form are being checked by validation.
    """

    instance = MagicMock()
    data = {
        "email": "hello@world.com",
        "password_1": "Hello",
    }
    form = EmailUserOptionalFieldsForm(data=data, instance=instance)

    assert form.is_valid() is False
    assert (
        form.errors.as_json()
        == '{"__all__": [{"message": "Provide both of passwords", "code": "provide_both_passwords"}]}'
    )


def test_not_matching_passwords():
    """
    Test whether 2 different password fields within the form are being validated.
    """

    instance = MagicMock()
    data = {
        "email": "hello@world.com",
        "password_1": "Hello",
        "password_2": "World",
    }
    form = EmailUserOptionalFieldsForm(data=data, instance=instance)

    assert form.is_valid() is False
    assert (
        form.errors.as_json()
        == '{"__all__": [{"message": "Passwords should be same", "code": "password_should_be_same"}]}'
    )


def test_matching_passwords():
    """
    Test whether 2 same password fields within the form are being valid and accepted.
    """

    instance = MagicMock()
    data = {
        "email": "hello@world.com",
        "password_1": "Hello",
        "password_2": "Hello",
    }
    form = EmailUserOptionalFieldsForm(data=data, instance=instance)

    assert form.is_valid() is True
