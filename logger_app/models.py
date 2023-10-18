from django.db import models

from customers_app.models import Customer
from service_app.models import Mailing


NULLABLE = {'blank': True, 'null': True}


class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    last_attempt = models.DateTimeField(verbose_name='дата и время последней попытки')
    attempt_status = models.CharField(max_length=20, verbose_name='статус попытки')
    server_response = models.IntegerField(**NULLABLE, verbose_name='ответ почтового сервера, если он был')

    def __str__(self):
        return self.last_attempt

    class Meta:
        verbose_name = 'попытку'
        verbose_name_plural = 'попытки'
