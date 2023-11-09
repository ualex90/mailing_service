from django.core.management import BaseCommand

from blog_app.models import Post
from main_app.utils import get_random_list


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print(get_random_list(Post))
