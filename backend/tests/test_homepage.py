import pytest
from tests.fixtures.fixture_api_client import api_client  # noqa


@pytest.mark.django_db()
def test_view_unauthorized(api_client):
    url = '/api/recipes/'
    response = api_client.get(url)
    assert response.status_code == 200
