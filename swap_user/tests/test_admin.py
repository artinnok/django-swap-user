from django.test import Client

import pytest


@pytest.mark.django_db
def test_to_email_otp_login(to_email_otp_settings):
    """
    Check that `to_email_otp` admin login page loads successfully.
    """

    client = Client()

    response = client.get("/admin/login/")
    assert response.status_code == 200
