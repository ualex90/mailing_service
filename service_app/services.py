import smtplib

from django.core.mail import send_mass_mail

import service_app
from config.settings import EMAIL_HOST
from customers_app.models import Customer
from logger_app.models import MailingLog
from service_app.models import Mailing


def send_mailing(pk: int) -> None:
    """отправка сообщений подписанным на рассылку пользователям"""
    attempt_status = 'Ошибка'
    server_response = str()

    # формирование сообщений
    mailing = Mailing.objects.get(pk=pk)
    message_list = get_message_list(mailing)

    # отправка сообщений
    try:
        send_mass_mail(message_list, fail_silently=False)
    except smtplib.SMTPSenderRefused:
        server_response = 'Адрес отправителя отклонен: он не принадлежит авторизующемуся пользователю'
    except smtplib.SMTPAuthenticationError:
        server_response = 'Ошибка авторизации. Неправильное имя пользователя или пароль'
    except OSError:
        server_response = f'Хост ({EMAIL_HOST}) недоступен'
    else:
        attempt_status = 'Успешно'

    # Запись лога
    MailingLog.objects.create(
        mailing=mailing,
        attempt_status=attempt_status,
        server_response=server_response
    )


def get_message_list(mailing: Mailing) -> list:
    """Создание списка сообщений"""

    message_list = list()
    for customer in Customer.objects.all():
        try:
            customer.subscriptions.get(pk=mailing.pk)
        except service_app.models.Mailing.DoesNotExist:
            pass
        else:
            if customer.is_mailing:
                body = (f'Привет {customer.first_name}!\n'
                        f'{mailing.body} \n\n'
                        f'Данное сообщение сформировано автоматически. Просьба не отвечать.')
                message = (mailing.title,
                           body,
                           None,
                           [customer.email])
                message_list.append(message)
    return message_list
