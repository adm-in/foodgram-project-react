import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUsersAuth:
    url_register = '/api/auth/users/'
    url_login = '/api/auth/token/login/'
    url_logout = '/api/auth/token/logout/'
    url_change_pass = '/api/users/set_password/'

    user_dict = dict(
        username='test_user2',
        password='!Qwerty1232',
        email='test2@gmail.com',
        first_name='Test2',
        last_name='Testov2',
    )

    @pytest.mark.django_db(transaction=True)
    def test_registration(self, foodgram_user, first_user, foodgram_client):
        response = foodgram_client.post(self.url_register, self.user_dict)

        assert foodgram_user.username == first_user.username
        assert foodgram_user.check_password('!Qwerty123')
        assert foodgram_user.email == first_user.email
        assert foodgram_user.first_name == first_user.first_name
        assert foodgram_user.last_name == first_user.last_name
        assert isinstance(first_user, User)

        assert response.status_code != 400, (
            f'Проверьте, что при POST запросе`{self.url_register}` '
            'не возвращается статус 400. Обязательное поле не заполнено!'
        )

        assert response.status_code == 201, (
            f'Проверьте, что при POST запросе`{self.url_register}` '
            'возвращается статус 201 '
        )

        assert User.objects.count() == 2

    @pytest.mark.django_db(transaction=True)
    def test_login(self, foodgram_user, foodgram_client):
        response = foodgram_client.post(
            self.url_login,
            dict(email=foodgram_user.email, password='!Qwerty123'),
        )

        assert response.status_code == 200, (
            f'Проверьте, что при POST запросе`{self.url_login}` '
            'возвращается статус 200 '
        )

    @pytest.mark.django_db(transaction=True)
    def test_logout(self, foodgram_client_auth):
        response = foodgram_client_auth.post(self.url_logout)

        assert response.status_code != 403, (
            f'Проверьте, что при POST запросе`{self.url_logout}` '
            'не возвращается статус 403. Учетные данные не были предоставлены!'
        )
        assert response.status_code == 204, (
            f'Проверьте, что при POST запросе`{self.url_logout}` '
            'возвращается статус 204 '
        )

    @pytest.mark.django_db(transaction=True)
    def test_change_password(self, foodgram_user, foodgram_client_auth):
        response = foodgram_client_auth.post(
            self.url_change_pass,
            dict(current_password='!Qwerty123', new_password='!!123Qwerty?'),
        )
        user = User.objects.filter(username=foodgram_user.username).first()

        assert response.status_code != 400, (
            f'Проверьте, что при POST запросе`{self.url_change_pass}` '
            'не возвращается статус 400. Обязательное поле не заполнено!'
        )

        assert response.status_code != 403, (
            f'Проверьте, что при POST запросе`{self.url_change_pass}` '
            'не возвращается статус 403. Учетные данные не были предоставлены!'
        )

        assert response.status_code == 204, (
            f'Проверьте, что при POST запросе`{self.url_change_pass}` '
            'возвращается статус 204'
        )

        assert user.check_password('!!123Qwerty?'), (
            f'Убедитесь, что при POST запросе`{self.url_change_pass}` '
            'меняется пароль'
        )
