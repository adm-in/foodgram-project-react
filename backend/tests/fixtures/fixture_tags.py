import pytest


@pytest.fixture()
def tags_list():
    from recipes.models import Tag

    data = [
        {'id': 1, 'name': 'Завтрак', 'slug': 'breakfast', 'color': '#E26C2D'},
        {'id': 2, 'name': 'Обед', 'slug': 'lunch', 'color': '#32CD32'},
        {'id': 3, 'name': 'Ужин', 'slug': 'dinner', 'color': '#000080'},
    ]
    for tag in data:
        id, name, slug, color = tag.values()
        Tag.objects.create(id=id, name=name, slug=slug, color=color)
    return data
