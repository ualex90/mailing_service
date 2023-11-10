from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Contact(models.Model):
    country = models.CharField(max_length=50, verbose_name='Страна')
    inn = models.IntegerField(verbose_name='ИНН')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    phone = models.CharField(max_length=50, verbose_name='Телефон')

    def __str__(self):
        return f'{self.address}'

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'


class Message(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(**NULLABLE, max_length=20, verbose_name='Телефон')
    email = models.CharField(**NULLABLE, max_length=100, verbose_name='email')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'{self.name} {self.phone} {self.email}'

    class Meta:
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщение'
