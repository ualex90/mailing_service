from django.utils.timezone import now
from django.views.generic import TemplateView

from blog_app.models import Post
from customers_app.models import Customer
from main_app.utils import get_random_list
from service_app.models import Mailing
from users_app.models import User


class IndexView(TemplateView):
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        # Количество пользователей сервиса
        context_data['user_count'] = User.objects.count()

        # Количество рассылок всего
        context_data['mailing_count'] = Mailing.objects.count()

        # Количество активных рассылок
        context_data['mailing_active_count'] = (Mailing.objects.
                                                filter(start_time__lte=now()).
                                                exclude(status=Mailing.PAUSED).
                                                exclude(status=Mailing.COMPLETED).
                                                exclude(is_active=False).count())

        # Количество уникальных клиентов для рассылок
        customers = set(map(str, Customer.objects.all()))
        print(customers)
        context_data['customer_count'] = len(customers)

        # 3 случайных записи из блога
        context_data['post_list'] = get_random_list(Post)

        return context_data
