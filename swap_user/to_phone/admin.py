from django.contrib import admin

from swap_user.admin import BaseUserAdmin
from swap_user.to_phone.forms import AddPhoneUserForm, EditPhoneUserForm
from swap_user.to_phone.models import PhoneUser


class PhoneUserAdmin(BaseUserAdmin):
    """
    Admin class with overridden `add` and `edit` forms.
    """

    add_form_class = AddPhoneUserForm
    change_form_class = EditPhoneUserForm


admin.site.register(PhoneUser, PhoneUserAdmin)
