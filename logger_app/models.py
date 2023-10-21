from django.db import models


NULLABLE = {'blank': True, 'null': True}


class MailingLog(models.Model):
    mailing = models.ForeignKey('service_app.Mailing', on_delete=models.CASCADE, verbose_name='рассылка')
    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    attempt_status = models.CharField(max_length=20, verbose_name='статус попытки')
    server_response = models.CharField(**NULLABLE, max_length=250, verbose_name='ответ почтового сервера, если он был')

    def __str__(self):
        return self.last_attempt

    class Meta:
        verbose_name = 'попытку'
        verbose_name_plural = 'попытки отправки писем'
