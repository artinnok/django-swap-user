from django.contrib import admin

from swap_user.admin import BaseUserAdmin
from swap_user.to_named_email.forms import (
    NamedUserEmailOptionalFieldsForm,
    NamedUserEmailRequiredFieldsForm,
)
from swap_user.to_named_email.models import NamedEmailUser


class NamedEmailUserAdmin(BaseUserAdmin):
    add_form_class = NamedUserEmailRequiredFieldsForm
    change_form_class = NamedUserEmailOptionalFieldsForm


admin.site.register(NamedEmailUser, NamedEmailUserAdmin)
