# Generated by Django 4.2.6 on 2023-10-22 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0002_alter_mailing_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='stop_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='окончание рассылки'),
        ),
    ]