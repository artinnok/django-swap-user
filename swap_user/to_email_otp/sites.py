from django.contrib import admin

from swap_user.to_email_otp.forms import OTPUserAuthenticationForm


class EmailOTPUserSite(admin.AdminSite):
    # Order of templates is crucial
    # Ref - https://docs.djangoproject.com/en/4.0/ref/templates/api/#django.template.loaders.app_directories.Loader
    login_form = OTPUserAuthenticationForm
