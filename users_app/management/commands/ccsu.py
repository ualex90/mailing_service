from django.core.management import BaseCommand

from users_app.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        user.set_password('admin')
        user.save()