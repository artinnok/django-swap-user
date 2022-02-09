from django.contrib import admin
from django.views.decorators.cache import never_cache

from swap_user.to_email_otp.views import GetOTPView


class EmailOTPUserSite(admin.AdminSite):
    # Order of templates is crucial
    # Ref - https://docs.djangoproject.com/en/4.0/ref/templates/api/#django.template.loaders.app_directories.Loader

    @never_cache
    def login(self, request, extra_context=None):
        request.current_app = self.name

        context = {
            **self.each_context(request),
            **(extra_context or {}),
        }
        defaults = {
            'extra_context': context,
        }
        # end of copied part

        return GetOTPView.as_view(**defaults)(request)
