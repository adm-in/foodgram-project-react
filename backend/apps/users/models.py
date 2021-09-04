from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты', unique=True,
    )
    username = models.CharField(
        verbose_name='Логин', max_length=150, unique=True,
    )
    first_name = models.CharField(verbose_name='Имя', max_length=150,)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150,)
    #is_favorited = models.BooleanField(blank=True)
    #is_subscribed = models.BooleanField(blank=True)

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username
