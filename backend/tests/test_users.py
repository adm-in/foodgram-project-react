import pytest


class TestUserLoginLogout:
    url_register = '/api/auth/users/'
    url_login = '/api/auth/token/login/'
    url_logout = '/api/auth/token/logout/'

    user_dict = dict(
        username='test_user2',
        password='!Qwerty1232',
        email='test2@gmail.com',
        first_name='Test2',
        last_name='Testov2',
    )

    @pytest.mark.django_db(transaction=True)
    def test_registration(self, foodgram_user, foodgram_client):
        assert 'test_user' == foodgram_user.username
        assert foodgram_user.check_password('!Qwerty123')
        assert 'test@gmail.com' == foodgram_user.email
        assert 'Test' == foodgram_user.first_name
        assert 'Testov' == foodgram_user.last_name

        response = foodgram_client.post(self.url_register, self.user_dict)

        data = response.data

        assert data['first_name'] == self.user_dict['first_name']
        assert response.status_code == 201
