import secrets
import string

from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта',
        help_text='Введите электронную почту'
    )
    avatar = models.ImageField(
        upload_to='image/avatars',
        verbose_name='Аватар',
        default="image/avatars/def_avatar.jpg"
    )
    nickname = models.CharField(
        max_length=100,
        verbose_name='Ник'
    )
    token = models.CharField(
        max_length=100,
        verbose_name="Токен",
        **NULLABLE
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def make_token(self):
        self.token = secrets.token_hex(16)

    def set_password(self, raw_password=None):
        if raw_password:
            super().set_password(raw_password)
        else:
            alphabet = string.ascii_letters + string.digits
            raw_password = ''.join(secrets.choice(alphabet) for i in range(8))
            super().set_password(raw_password)
            return raw_password


class Log(models.Model):
    time = models.DateTimeField(verbose_name='Дата и время попытки отправки', auto_now_add=True)
    status = models.BooleanField(verbose_name='Статус попытки отправки')
    server_response = models.CharField(max_length=150, verbose_name='Ответ почтового сервера', **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f' {self.time}, {self.status}, {self.server_response}'

    class Meta:
        verbose_name = "Попытка отправки сообщения"
        verbose_name_plural = "Попытки отправки сообщения"
