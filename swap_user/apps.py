from django.contrib.admin import apps


class DjangoSwapUser(apps.AppConfig):
    """
    This is default app config
    """

    name = "swap_user"
    verbose_name = "Django Swap User"


class OTPSiteConfig(apps.AdminConfig):
    """
    This config required for customizing admin panel Login form.
    """

    # custom admin site with customized Login form.
    default_site = "swap_user.otp.sites.OTPUserSite"
