from django.contrib.auth.models import AbstractUser, UserManager
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
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь',
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='Владелец аккаунта',
    )

    class Meta:
        verbose_name = 'Подписка'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'owner'], name='unique_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} => {self.author}'
