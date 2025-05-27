from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_usr(api_client):
    def do_auth_usr(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_auth_usr