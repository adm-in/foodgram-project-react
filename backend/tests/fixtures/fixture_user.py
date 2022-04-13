import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
def user():
    return User.objects.create_user(
        username='test_user',
        password='!Qwerty123',
        email='test@gmail.com',
        first_name='Test',
        last_name='Testov',
    )


@pytest.fixture()
def user_client(user, client):
    client.force_login(user)
    return client
