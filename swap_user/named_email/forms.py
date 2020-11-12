from swap_user.forms import BaseUserForm
from swap_user.named_email.models import NamedEmailUser


class NamedUserEmailForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        model = NamedEmailUser
