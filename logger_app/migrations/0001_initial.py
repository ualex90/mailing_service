# Generated by Django 4.2.6 on 2023-10-21 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_attempt', models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')),
                ('attempt_status', models.CharField(max_length=20, verbose_name='статус попытки')),
                ('server_response', models.CharField(blank=True, max_length=250, null=True, verbose_name='ответ почтового сервера, если он был')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_app.mailing', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'попытку',
                'verbose_name_plural': 'попытки отправки писем',
            },
        ),
    ]
