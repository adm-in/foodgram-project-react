import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
def foodgram_user():
    return User.objects.create_user(
        username='test_user',
        password='!Qwerty123',
        email='test@gmail.com',
        first_name='Test',
        last_name='Testov',
    )


@pytest.fixture()
def foodgram_token(foodgram_user):
    from rest_framework.authtoken.models import Token

    Token.objects.create(user=foodgram_user)
    return Token.objects.get(user=foodgram_user)


@pytest.fixture()
def foodgram_client(foodgram_token):
    from rest_framework.test import APIClient

    client = APIClient()
    return client


@pytest.fixture()
def foodgram_client_auth(foodgram_token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + foodgram_token.key)
    return client
