import os

from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        os.system("python3 manage.py loaddata fixtures/db.json")

