from swap_user.base_forms import BaseUserOptionalFieldsForm, BaseUserRequiredFieldsForm
from swap_user.to_email.models import EmailUser


class EmailUserOptionalFieldsForm(BaseUserOptionalFieldsForm):
    """
    Form for - EmailUser model.
    With optional `password_1` and `password_2` fields.
    """

    class Meta(BaseUserOptionalFieldsForm.Meta):
        model = EmailUser


class EmailUserRequiredFieldsForm(BaseUserRequiredFieldsForm):
    """
    Form for - EmailUser model.
    With required `password_1` and `password_2` fields.
    """

    class Meta(BaseUserRequiredFieldsForm.Meta):
        model = EmailUser
