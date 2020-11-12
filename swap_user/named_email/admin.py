from django.contrib import admin

from swap_user.named_email.forms import NamedUserEmailForm
from swap_user.named_email.models import NamedEmailUser


class NamedEmailUserAdmin(admin.ModelAdmin):
    form = NamedUserEmailForm


admin.site.register(NamedEmailUser, NamedEmailUserAdmin)
