from swap_user.email.models import EmailUser
from swap_user.forms import BaseUserForm


class EmailUserForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        model = EmailUser
