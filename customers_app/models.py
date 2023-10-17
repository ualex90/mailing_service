from django.db import models


class Customer(models.Model):
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    first_name = models.CharField(max_length=150, verbose_name='имя')
    surname = models.CharField(max_length=150, blank=True, null=True, verbose_name='отчество')
    email = models.EmailField(max_length=100, verbose_name='email')
    comment = models.TextField(blank=True, null=True, verbose_name='комментарий')
    is_mailing = models.BooleanField(default=True, verbose_name='подписка на рассылку')

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.surname}'

    class Meta:
        verbose_name = 'клиента'
        verbose_name_plural = 'клиенты'
