from django.db import models


NULLABLE = {'blank': True, 'null': True}


class MailingLog(models.Model):
    AUTO = 'A'
    MANUAL = 'M'

    MODE_CHOICES = [
        (AUTO, 'Автоматический'),
        (MANUAL, 'Ручной'),
    ]

    mailing = models.ForeignKey('service_app.Mailing', on_delete=models.CASCADE, verbose_name='рассылка')
    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    server_response = models.CharField(**NULLABLE, max_length=250, verbose_name='ответ почтового сервера, если он был')
    is_successfully = models.BooleanField(default=False, verbose_name='статус попытки')
    mode = models.CharField(**NULLABLE, max_length=1, choices=MODE_CHOICES, verbose_name='режим отправки')

    def __str__(self):
        return self.last_attempt

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Рассылки'
