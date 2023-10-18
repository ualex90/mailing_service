from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    name = models.CharField(max_length=150, verbose_name='название рассылки')
    title = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    periodicity = models.CharField(max_length=5, verbose_name='периодичность')  # day, week, month
    mailing_time = models.TimeField(verbose_name='время рассылки')
    status = models.CharField(**NULLABLE, max_length=10, verbose_name='статус')  # completed, created, launched

    def __str__(self):
        return f'{self.name} ({self.periodicity})'

    class Meta:
        verbose_name = 'рассылку'
        verbose_name_plural = 'рассылки'


class Log(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    last_attempt = models.DateTimeField(**NULLABLE, verbose_name='дата и время последней попытки')
    attempt_status = models.CharField(**NULLABLE, max_length=20, verbose_name='статус попытки')
    server_response = models.IntegerField(**NULLABLE, verbose_name='ответ почтового сервера, если он был')

    def __str__(self):
        return self.last_attempt

    class Meta:
        verbose_name = 'попытку'
        verbose_name_plural = 'попытки'
