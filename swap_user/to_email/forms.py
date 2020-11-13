from swap_user.forms import BaseUserForm
from swap_user.to_email.models import EmailUser


class EmailUserForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        model = EmailUser
