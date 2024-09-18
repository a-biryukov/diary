from django.db import models

from config.settings import NULLABLE, AUTH_USER_MODEL


class Entry(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок',
        help_text='Введите заголовок',
        **NULLABLE
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст',
        **NULLABLE
    )
    published_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        **NULLABLE
    )
    changed_at = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name='Владелец',
        on_delete=models.CASCADE,
        **NULLABLE
    )

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.title if self.title else self.text
