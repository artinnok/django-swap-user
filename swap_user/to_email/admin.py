from django.contrib import admin

from swap_user.to_email.forms import EmailUserForm
from swap_user.to_email.models import EmailUser


class EmailUserAdmin(admin.ModelAdmin):
    form = EmailUserForm


admin.site.register(EmailUser, EmailUserAdmin)
