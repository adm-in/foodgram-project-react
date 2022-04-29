import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUsers:
    url_user = '/api/users/{id}/'
    url_users = '/api/users/'
    url_profile = '/api/users/me/'

    user_dict = dict(
        username='test_user2',
        password='!Qwerty1232',
        email='test2@gmail.com',
        first_name='Test2',
        last_name='Testov2',
    )

    @pytest.mark.django_db(transaction=True)
    def test_get_user(self,):
        pass

    @pytest.mark.django_db(transaction=True)
    def test_get_users(self,):
        pass

    @pytest.mark.django_db(transaction=True)
    def test_get_profile(self):
        pass
