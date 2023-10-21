from django.core.mail import send_mass_mail

import service_app
from customers_app.models import Customer
from service_app.models import Mailing


def send_mailing(pk: int) -> None:
    mailing = Mailing.objects.get(pk=pk)
    message_list = list()
    for customer in Customer.objects.all():
        try:
            customer.subscriptions.get(pk=pk)
        except service_app.models.Mailing.DoesNotExist:
            pass
        else:
            if customer.is_mailing:
                message = (mailing.title,
                           f'Привет {customer.first_name}!\n{mailing.body}',
                           None,
                           [customer.email])
                message_list.append(message)

    send_mass_mail(message_list, fail_silently=False)
