import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUsers:
    url_user_1 = '/api/users/6/'
    url_user_2 = '/api/users/7/'
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
    def test_get_user(
        self, foodgram_user, foodgram_user2, foodgram_client_auth,
    ):
        user_1 = foodgram_client_auth.get(self.url_user_1)

        assert foodgram_user.username == user_1.data['username']
        assert foodgram_user.check_password('!Qwerty123')
        assert foodgram_user.email == user_1.data['email']
        assert foodgram_user.first_name == user_1.data['first_name']
        assert foodgram_user.last_name == user_1.data['last_name']

        user_2 = foodgram_client_auth.get(self.url_user_2)

        assert foodgram_user2.username == user_2.data['username']
        assert foodgram_user2.check_password('!Qwerty321!')
        assert foodgram_user2.email == user_2.data['email']
        assert foodgram_user2.first_name == user_2.data['first_name']
        assert foodgram_user2.last_name == user_2.data['last_name']

        assert user_1.status_code != 403, (
            f'Проверьте, что при GET запросе`{self.url_user_1}` '
            'не возвращается статус 403. Учетные данные не были предоставлены!'
        )

        assert user_2.status_code != 403, (
            f'Проверьте, что при GET запросе`{self.url_user_2}` '
            'не возвращается статус 403. Учетные данные не были предоставлены!'
        )

        assert user_1.status_code != 404, (
            f'Проверьте, что при GET запросе`{self.url_user_1}` '
            'не возвращается статус 404. Страница не найдена!'
        )

        assert user_2.status_code != 404, (
            f'Проверьте, что при GET запросе`{self.url_user_2}` '
            'не возвращается статус 404. Страница не найдена!'
        )

        assert user_1.status_code == 200, (
            f'Проверьте, что при GET запросе`{self.url_user_1}` '
            'возвращается статус 200'
        )

        assert user_2.status_code == 200, (
            f'Проверьте, что при GET запросе`{self.url_user_2}` '
            'возвращается статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_get_users(self):
        pass

    @pytest.mark.django_db(transaction=True)
    def test_get_profile(self):
        pass
