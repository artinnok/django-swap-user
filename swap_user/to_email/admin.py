from django.contrib import admin

from swap_user.admin import BaseUserAdmin
from swap_user.to_email.forms import EmailUserOptionalFieldsForm, EmailUserRequiredFieldsForm
from swap_user.to_email.models import EmailUser


class EmailUserAdmin(BaseUserAdmin):
    add_form_class = EmailUserRequiredFieldsForm
    change_form_class = EmailUserOptionalFieldsForm


admin.site.register(EmailUser, EmailUserAdmin)
