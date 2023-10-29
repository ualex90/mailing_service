from django.core.management import BaseCommand

from users_app.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin = User.objects.get(email='admin@sky.pro')
        admin.set_password('admin')
        admin.save()
