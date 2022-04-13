import pytest
from django.contrib.auth import get_user_model
from tests.fixtures.fixture_user import user, user_client  # noqa

User = get_user_model()


@pytest.mark.django_db()
def test_user_create():
    User.objects.create_user(
        username='test_user',
        password='!Qwerty123',
        email='test@gmail.com',
        first_name='Test',
        last_name='Testov',
    )

    user = User.objects.filter(username='test_user').first()
    assert User.objects.count() == 1
    assert isinstance(user, User)
    assert user.check_password('!Qwerty123')
