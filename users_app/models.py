from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}

COUNTRY_CHOICES = {
    ('RU', 'Россия'),
    ('AM', 'Армения'),
    ('BY', 'Беларусь'),
    ('GE', 'Грузия'),
    ('KZ', 'Казахстан'),
    ('KG', 'Киргизия'),
    ('LV', 'Латвия'),
    ('LT', 'Литва'),
    ('MD', 'Молдова'),
    ('CK', 'Острова Кука'),
    ('UZ', 'Узбекистан'),
    ('OS', 'Южная Осетия'),
    ('XX', 'Другая страна'),
}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    first_name = models.CharField(**NULLABLE, max_length=35, verbose_name='Имя')
    last_name = models.CharField(**NULLABLE, max_length=35, verbose_name='Фамилия')
    surname = models.CharField(**NULLABLE, max_length=35, verbose_name='Отчество')
    phone = models.CharField(**NULLABLE, max_length=35, verbose_name='Номер телефона')
    telegram = models.CharField(**NULLABLE, max_length=30, verbose_name='Telegram')
    country = models.CharField(**NULLABLE, max_length=25, choices=COUNTRY_CHOICES, verbose_name='Страна')
    avatar = models.ImageField(**NULLABLE, verbose_name='Аватар')
    key = models.CharField(**NULLABLE, max_length=25, unique=True, verbose_name='Ключ пользователя')
    is_active = models.BooleanField(default=False, verbose_name='Активен')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('set_active', 'Блокировка пользователя>'),
        ]
