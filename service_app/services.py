import smtplib
from datetime import timedelta

from django.core.mail import send_mass_mail

from config.settings import EMAIL_HOST
from logger_app.models import MailingLog
from service_app.models import Mailing
from django.utils.timezone import now


def scheduled_send_mailing() -> None:
    """Фильтрация рассылок и их отправка в автоматическом режиме"""
    today = now()

    # Перебор рассылок с фильтрацией
    for mailing in (Mailing.objects.
                    filter(start_time__lte=today).
                    exclude(status=Mailing.PAUSED).
                    exclude(status=Mailing.COMPLETED).
                    exclude(is_active=False)):

        # Проверка на завершение рассылки. Если по времени окончена,
        # меняем статус на "Завершена" и идем к следующей рассылки
        if mailing.stop_time < today if mailing.stop_time else False:
            mailing.status = Mailing.COMPLETED
            mailing.save()
        else:
            # Если все условия совпали, проверяем время отправки и если пора, отправляем сообщений
            if mailing.send_time + timedelta(minutes=mailing.periodic) < today if mailing.send_time else True:
                send_mailing(mailing)


def send_mailing(mailing: Mailing, manual=None) -> None:
    """
    Оправка сообщений подписанным на рассылку пользователям.

    Если передан "manual=True", то определяется режим отправки как "Ручной"
    при этом не меняется статус и не фиксируется время отправки сообщения в модели рассылки
    """
    is_successfully = False
    server_response = str()

    # формирование сообщений
    message_list = get_message_list(mailing)
    # Отправка сообщений
    if message_list:
        try:
            send_mass_mail(message_list, fail_silently=False)
        except smtplib.SMTPSenderRefused:
            server_response = 'Адрес отправителя отклонен: он не принадлежит авторизующемуся пользователю'
        except smtplib.SMTPAuthenticationError:
            server_response = 'Ошибка авторизации. Неправильное имя пользователя или пароль'
        except OSError:
            server_response = f'Хост ({EMAIL_HOST}) недоступен'
        else:
            is_successfully = True
            if not manual:
                mailing.status = mailing.LAUNCHED
                mailing.send_time = now().strftime('%Y-%m-%d %H:%M')
            mailing.save()
        # Запись лога
        print(f'Успешная рассылка "{mailing}"')
        MailingLog.objects.create(
            mailing=mailing,
            server_response=server_response,
            is_successfully=is_successfully,
            mode=MailingLog.MANUAL if manual else MailingLog.AUTO,
        )


def get_message_list(mailing: Mailing) -> list:
    """
    Проверяем, включена ли рассылка у пользователей и если да,
    формируем сообщение и добавляем его в список
    """
    message_list = list()
    for customer in mailing.customers.filter(is_mailing=True):
        body = (f'Привет {customer.first_name}!\n'
                f'{mailing.message.body} \n\n'
                f'Данное сообщение сформировано автоматически. Просьба не отвечать.')
        message = (mailing.message.title,
                   body,
                   None,
                   [customer.email])
        message_list.append(message)

    return message_list
