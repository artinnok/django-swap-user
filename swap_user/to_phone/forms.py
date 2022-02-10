from swap_user.base_forms import BaseUserOptionalFieldsForm, BaseUserRequiredFieldsForm
from swap_user.to_phone.models import PhoneUser


class EditPhoneUserForm(BaseUserOptionalFieldsForm):
    """
    Form for - PhoneUser model.
    With optional `password_1` and `password_2` fields.

    Suitable for edit user pages.
    """

    class Meta(BaseUserOptionalFieldsForm.Meta):
        model = PhoneUser


class AddPhoneUserForm(BaseUserRequiredFieldsForm):
    """
    Form for - PhoneUser model.
    With required `password_1` and `password_2` fields.

    Suitable for user add pages.
    """

    class Meta(BaseUserRequiredFieldsForm.Meta):
        model = PhoneUser
