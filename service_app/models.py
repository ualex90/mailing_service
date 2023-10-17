from django.db import models

from customers_app.models import Customer


class Mailing(models.Model):
    name = models.CharField(max_length=150, verbose_name='название рассылки')
    title = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    periodicity = models.CharField(max_length=5, verbose_name='периодичность')  # day, week, month
    mailing_time = models.TimeField(verbose_name='время рассылки')
    customers = models.ManyToManyField(Customer, verbose_name='клиенты')
    status = models.CharField(max_length=10, blank=True, null=True, verbose_name='статус')  # completed, created, launched

    def __str__(self):
        return f'{self.mailing_time} {self.periodicity}'

    class Meta:
        verbose_name = 'рассылку'
        verbose_name_plural = 'рассылки'


class Log(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    last_attempt = models.DateTimeField(blank=True, null=True, verbose_name='дата и время последней попытки')
    attempt_status = models.CharField(max_length=20, blank=True, null=True, verbose_name='статус попытки')
    server_response = models.IntegerField(blank=True, null=True, verbose_name='ответ почтового сервера, если он был')

    def __str__(self):
        return self.last_attempt

    class Meta:
        verbose_name = 'попытку'
        verbose_name_plural = 'попытки'
