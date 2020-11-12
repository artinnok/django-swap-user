from django.contrib import admin

from swap_user.email.forms import EmailUserForm
from swap_user.email.models import EmailUser


class EmailUserAdmin(admin.ModelAdmin):
    form = EmailUserForm


admin.site.register(EmailUser, EmailUserAdmin)
