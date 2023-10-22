# Generated by Django 4.2.6 on 2023-10-22 06:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0007_alter_mailing_periodic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='periodic',
            field=models.CharField(choices=[(datetime.timedelta(seconds=60), 'Минута'), (datetime.timedelta(seconds=3600), 'Час'), (datetime.timedelta(days=1), 'День'), (datetime.timedelta(days=7), 'Неделя'), (datetime.timedelta(days=30), 'Месяц'), (datetime.timedelta(days=365), 'Год')], default=datetime.timedelta(days=1), max_length=30, verbose_name='периодичность'),
        ),
    ]
