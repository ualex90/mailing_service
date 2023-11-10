import os

from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        os.system("python3 manage.py dumpdata users_app > fixtures/users_app.json")
        os.system("python3 manage.py dumpdata main_app > fixtures/main_app.json")
        os.system("python3 manage.py dumpdata service_app > fixtures/service_app.json")
        os.system("python3 manage.py dumpdata customers_app > fixtures/customers_app.json")
        os.system("python3 manage.py dumpdata logger_app > fixtures/logger_app.json")
        os.system("python3 manage.py dumpdata blog_app > fixtures/blog_app.json")

