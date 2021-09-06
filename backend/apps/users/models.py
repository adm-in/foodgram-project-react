from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField(
        verbose_name='Адрес электронной почты', unique=True,
    )
    username = models.CharField(
        verbose_name='Логин', max_length=150, unique=True,
    )
    first_name = models.CharField(verbose_name='Имя', max_length=150, )
    last_name = models.CharField(verbose_name='Фамилия', max_length=150, )

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username

# class Subscribe(models.Model):
