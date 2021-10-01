from django.contrib import admin

from swap_user.admin import BaseUserAdmin
from swap_user.to_phone_otp.forms import AddPhoneUserForm, EditPhoneUserForm
from swap_user.to_phone_otp.models import PhoneOTPUser


class PhoneOTPUserAdmin(BaseUserAdmin):
    """
    Admin class with overridden `add` and `edit` forms.
    """

    add_form_class = AddPhoneUserForm
    change_form_class = EditPhoneUserForm


admin.site.register(PhoneOTPUser, PhoneOTPUserAdmin)
