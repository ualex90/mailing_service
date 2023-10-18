from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Periodicity(models.Model):
    name = models.CharField(max_length=10, verbose_name='периодичность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'периодичность'
        verbose_name_plural = 'периодичности'


class Mailing(models.Model):
    name = models.CharField(max_length=25, verbose_name='название рассылки')
    title = models.CharField(max_length=100, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    periodicity = models.ForeignKey(Periodicity, on_delete=models.CASCADE, verbose_name='периодичность')
    mailing_time = models.TimeField(verbose_name='время рассылки')
    status = models.CharField(**NULLABLE, max_length=10, verbose_name='статус')  # completed, created, launched
    is_active = models.BooleanField(default=True, verbose_name='включить')

    def __str__(self):
        return f'{self.name} ({self.periodicity})'

    class Meta:
        verbose_name = 'рассылку'
        verbose_name_plural = 'рассылки'
