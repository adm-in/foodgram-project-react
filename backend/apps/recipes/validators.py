from django.core.exceptions import ValidationError


def cooking_time_validator(value):
    if value <= 0 or value > 999:
        raise ValidationError(
            f'Время приготовления: {value} указано некорректно.',
        )


def amount_validator(value):
    if value <= 0 or value > 999:
        raise ValidationError(
            f'Количество ингредиента: {value} указано некорректно.',
        )
