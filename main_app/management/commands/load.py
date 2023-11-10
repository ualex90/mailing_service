import os

from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        os.system("python3 manage.py loaddata fixtures/db.json")
        # os.system("python3 manage.py loaddata fixtures/auth_grope.json")
        # os.system("python3 manage.py loaddata fixtures/users_app.json")
        # os.system("python3 manage.py loaddata main_app > fixtures/main_app.json")
        # os.system("python3 manage.py loaddata service_app > fixtures/service_app.json")
        # os.system("python3 manage.py loaddata customers_app > fixtures/customers_app.json")
        # os.system("python3 manage.py loaddata logger_app > fixtures/logger_app.json")
        # os.system("python3 manage.py loaddata blog_app > fixtures/blog_app.json")

