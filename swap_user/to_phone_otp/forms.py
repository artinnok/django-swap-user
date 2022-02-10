from swap_user.base_forms import BaseUserOptionalFieldsForm, BaseUserRequiredFieldsForm
from swap_user.to_phone_otp.models import PhoneOTPUser


class EditPhoneUserForm(BaseUserOptionalFieldsForm):
    """
    Form for - PhoneOTPUser model.
    With optional `password_1` and `password_2` fields.

    Suitable for edit user pages.
    """

    class Meta(BaseUserOptionalFieldsForm.Meta):
        model = PhoneOTPUser


class AddPhoneUserForm(BaseUserRequiredFieldsForm):
    """
    Form for - PhoneOTPUser model.
    With required `password_1` and `password_2` fields.

    Suitable for user add pages.
    """

    class Meta(BaseUserRequiredFieldsForm.Meta):
        model = PhoneOTPUser
