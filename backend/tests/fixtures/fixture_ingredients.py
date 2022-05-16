import pytest


@pytest.fixture()
def ingredients_list():
    from recipes.models import Ingredient

    data = [
        {'id': 1, 'name': 'сок', 'measurement_unit': 'л'},
        {'id': 2, 'name': 'огурцы', 'measurement_unit': 'кг'},
        {'id': 3, 'name': 'сахар', 'measurement_unit': 'гр'},
    ]
    for ingredient in data:
        id, name, measurement_unit = ingredient.values()
        Ingredient.objects.create(
            id=id, name=name, measurement_unit=measurement_unit
        )
    return data
