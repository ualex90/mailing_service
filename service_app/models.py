from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Periodicity(models.Model):
    name = models.CharField(max_length=10, verbose_name='периодичность')
    minutes = models.IntegerField(default=0, validators=[MaxValueValidator(60)], verbose_name='минуты')
    hours = models.IntegerField(default=0, validators=[MaxValueValidator(24)], verbose_name='часы')
    days = models.IntegerField(default=7, validators=[MaxValueValidator(360)], verbose_name='дни')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'периодичность'
        verbose_name_plural = 'периодичность'


class Mailing(models.Model):
    name = models.CharField(max_length=25, verbose_name='название рассылки')
    title = models.CharField(max_length=100, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    periodicity = models.ForeignKey(Periodicity, on_delete=models.CASCADE, verbose_name='периодичность')
    start_time = models.TimeField(default='00:00:00', verbose_name='время начала')  # время старта
    stop_time = models.TimeField(default='00:10:00', verbose_name='длительность')  # Продолжительность выполнения попыток
    sending_time = models.DateTimeField(**NULLABLE, verbose_name='время успешной отправки')
    status = models.CharField(default='создана', max_length=10, verbose_name='статус')  # completed, created, launched
    is_active = models.BooleanField(default=True, verbose_name='включить')

    def __str__(self):
        return f'{self.name} ({self.periodicity})'

    class Meta:
        verbose_name = 'рассылку'
        verbose_name_plural = 'рассылки'
