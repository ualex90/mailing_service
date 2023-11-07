from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Post(models.Model):
    owner = models.ForeignKey('users_app.User', **NULLABLE, on_delete=models.SET_NULL, verbose_name='Создатель')
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(**NULLABLE, max_length=150, verbose_name='slug')
    body = models.TextField(verbose_name='содержимое')
    image = models.ImageField(**NULLABLE, verbose_name='превью')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.created_at} {self.title}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        permissions = [
            ('manage_content', 'Контент менеджмент'),
        ]
