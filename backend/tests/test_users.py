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
        assert foodgram_user.username == 'test_user'
        assert foodgram_user.check_password('!Qwerty123')
        assert foodgram_user.email == 'test@gmail.com'
        assert foodgram_user.first_name == 'Test'
        assert foodgram_user.last_name == 'Testov'

        response = foodgram_client.post(self.url_register, self.user_dict)

        data = response.data

        assert data['username'] == self.user_dict['username']
        assert data['email'] == self.user_dict['email']
        assert data['first_name'] == self.user_dict['first_name']
        assert data['last_name'] == self.user_dict['last_name']

        assert response.status_code == 201, (
            f'Проверьте, что при POST запросе`{self.url_register}` '
            'возвращается статус 201'
        )
