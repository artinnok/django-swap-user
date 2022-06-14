import django
import pytest


def pytest_configure():
    """
        Pytest hook which updates django's settings
        suitable for testing.
    """

    from django.conf import settings

    settings.configure(
        SECRET_KEY='secret',
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        MIDDLEWARE=(
            "django.middleware.common.CommonMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ),
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "swap_user",
        ),
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.template.context_processors.static",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            },
        ]
    )

    django.setup()


@pytest.fixture
def to_email_otp_settings(settings):
    """
    Fixture providing settings configuration for `to_email_otp`
    adding all required apps and other variables.
    """

    # Lazy import is required to pass exception
    from django.contrib.sites.models import Site

    # Workaround to get rid of related issues when fetching admin page
    site = Site.objects.create(domain='testserver', name='testserver')
    site.save()

    settings.SECRET_KEY = 'secret'
    settings.DEBUG_PROPAGATE_EXCEPTIONS = True
    settings.DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
    settings.MIDDLEWARE = (
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    )
    settings.INSTALLED_APPS = (
        "swap_user.apps.OTPSiteConfig",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.staticfiles",
        "swap_user",
        "swap_user.to_email_otp",
    )
    settings.TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.template.context_processors.static",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]
    settings.STATIC_URL = '/static'
    settings.ROOT_URLCONF = 'swap_user.tests.urls'
    settings.AUTH_USER_MODEL = "swap_to_email_otp.EmailOTPUser"

    return settings
