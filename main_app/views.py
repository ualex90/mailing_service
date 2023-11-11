from django.core.cache import cache
from django.utils.timezone import now
from django.views.generic import TemplateView

from blog_app.models import Post
from config import settings
from customers_app.models import Customer
from main_app.models import Contact, Message
from main_app.utils import get_random_list
from service_app.models import Mailing
from users_app.models import User


class IndexView(TemplateView):
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if settings.CACHE_ENABLED:
            # Если кэширование включено, но идем в redis за нашими запросами
            user_count = cache.get('user_count')
            if user_count is None:
                user_count = User.objects.count()
                cache.set('user_count', user_count)

            mailing_count = cache.get('mailing_count')
            if mailing_count is None:
                mailing_count = Mailing.objects.count()
                cache.set('mailing_count', mailing_count)

            mailing_active_count = cache.get('mailing_active_count')
            if mailing_active_count is None:
                mailing_active_count = (Mailing.objects.
                                        filter(start_time__lte=now()).
                                        exclude(status=Mailing.PAUSED).
                                        exclude(status=Mailing.COMPLETED).
                                        exclude(is_active=False).count())
                cache.set('mailing_active_count', mailing_active_count)

            customers_all = cache.get('customers_all')
            if customers_all is None:
                customers_all = Customer.objects.all()
                cache.set('customers_all', customers_all)

            post_list = cache.get('post_list')
            if post_list is None:
                post_list = get_random_list(Post)
                cache.set('post_list', post_list)

        else:
            # Если кэширование выключено, идем сразу в базу данных
            user_count = User.objects.count()
            mailing_count = Mailing.objects.count()
            mailing_active_count = (Mailing.objects.
                                    filter(start_time__lte=now()).
                                    exclude(status=Mailing.PAUSED).
                                    exclude(status=Mailing.COMPLETED).
                                    exclude(is_active=False).count())
            customers_all = Customer.objects.all()
            post_list = get_random_list(Post)

        # Количество пользователей сервиса
        context_data['user_count'] = user_count

        # Количество рассылок всего
        context_data['mailing_count'] = mailing_count

        # Количество активных рассылок
        context_data['mailing_active_count'] = mailing_active_count

        # Количество уникальных клиентов для рассылок
        customers = set(map(str, customers_all))
        context_data['customer_count'] = len(customers)

        # 3 случайных записи из блога
        context_data['post_list'] = post_list

        return context_data


class ContactView(TemplateView):
    template_name = 'main_app/contact_view.html'
    extra_context = {
        'title': 'Контакты',
        'description': 'Наши адреса',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if settings.CACHE_ENABLED:
            contact_all = cache.get('contact_all')
            if contact_all is None:
                contact_all = Contact.objects.all()
                cache.set('contact_all', contact_all)

        context_data['object_list'] = Contact.objects.all()
        return context_data

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        name = self.request.POST.get('name')
        phone = self.request.POST.get('phone')
        email = self.request.POST.get('email')
        message = self.request.POST.get('message')
        Message.objects.create(name=name, phone=phone, email=email, message=message)
        return self.render_to_response(context)
