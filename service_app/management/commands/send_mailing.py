import datetime

from django.core.management import BaseCommand
from django.utils.timezone import now

from service_app.services import scheduled_send_mailing


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduled_send_mailing()
        print(str(now().replace(microsecond=True)))
