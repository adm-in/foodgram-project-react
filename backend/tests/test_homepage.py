import pytest

# При GET запросе на адрес /api/recipes/ должен выводиться список первых 6
# рецептов отсортированых по дате побликации. Главная страница доступна всем,
# в ответ должен приходить 200.


@pytest.fixture()
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.mark.django_db()
def test_view_unauthorized(api_client):
    url = '/api/recipes/'
    response = api_client.get(url)
    assert response.status_code == 200
