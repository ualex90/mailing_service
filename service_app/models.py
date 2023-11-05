from datetime import timedelta

from django.db import models
from django.utils.timezone import now

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    title = models.CharField(max_length=30, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey('users_app.User', **NULLABLE, on_delete=models.CASCADE, verbose_name='создал')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    # MINUTE = 'MIN'
    # HORSE = 'H'
    # DAY = 'D'
    # WEEK = 'W'
    # MONTH = 'M'
    # YEAR = 'Y'

    MINUTE = 1
    HORSE = 60
    DAY = HORSE * 24
    WEEK = DAY * 7
    MONTH = DAY * 30
    YEAR = DAY * 365

    PERIODIC_CHOICES = [
        (MINUTE, 'Минута'),
        (HORSE, 'Час'),
        (DAY, 'День'),
        (WEEK, 'Неделя'),
        (MONTH, 'Месяц'),
        (YEAR, 'Год'),
    ]

    CREATED = 'CR'
    LAUNCHED = 'LA'
    COMPLETED = 'CP'
    PAUSED = 'PA'

    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена'),
        (PAUSED, 'Пауза'),
    ]

    name = models.CharField(max_length=25, verbose_name='название рассылки')
    message = models.ForeignKey(Message, **NULLABLE, on_delete=models.CASCADE, verbose_name='Сообщение')
    periodic = models.IntegerField(choices=PERIODIC_CHOICES, default=DAY, verbose_name='периодичность')
    start_time = models.DateTimeField(default=now, verbose_name='начало рассылки')
    stop_time = models.DateTimeField(**NULLABLE, verbose_name='окончание рассылки')
    send_time = models.DateTimeField(**NULLABLE, verbose_name='последняя отправка')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=CREATED, verbose_name='статус')
    customers = models.ManyToManyField('customers_app.Customer', verbose_name='клиенты')
    owner = models.ForeignKey('users_app.User', **NULLABLE, on_delete=models.CASCADE, verbose_name='создал')

    def __str__(self):
        return f'{self.name} ({self.get_periodic_display()})'

    class Meta:
        verbose_name = 'рассылку'
        verbose_name_plural = 'рассылки'
