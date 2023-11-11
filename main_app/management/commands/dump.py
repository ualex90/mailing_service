import os

from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        os.system("python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > fixtures/db.json")

