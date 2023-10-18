from django.db import models

from service_app.models import Mailing


NULLABLE = {'blank': True, 'null': True}


class Customer(models.Model):
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    first_name = models.CharField(max_length=150, verbose_name='имя')
    surname = models.CharField(**NULLABLE, max_length=150, verbose_name='отчество')
    email = models.EmailField(max_length=100, verbose_name='email')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')
    subscriptions = models.ManyToManyField(Mailing, **NULLABLE, verbose_name='подписки')

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.surname}'

    class Meta:
        verbose_name = 'клиента'
        verbose_name_plural = 'клиенты'
