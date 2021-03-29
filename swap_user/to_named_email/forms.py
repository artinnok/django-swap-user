from swap_user.forms import BaseUserOptionalFieldsForm, BaseUserRequiredFieldsForm
from swap_user.to_named_email.models import NamedEmailUser


class NamedUserEmailOptionalFieldsForm(BaseUserOptionalFieldsForm):
    """
    Form for - NamedEmailUser model.
    With required `password_1` and `password_2` fields.
    """

    class Meta(BaseUserOptionalFieldsForm.Meta):
        model = NamedEmailUser


class NamedUserEmailRequiredFieldsForm(BaseUserRequiredFieldsForm):
    """
    Form for - NamedEmailUser model.
    With required `password_1` and `password_2` fields.
    """

    class Meta(BaseUserRequiredFieldsForm.Meta):
        model = NamedEmailUser
