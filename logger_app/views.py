from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView

from logger_app.models import MailingLog
from service_app.models import Mailing


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog
    queryset = MailingLog.objects.filter().order_by('pk').reverse()
    paginate_by = 10
    extra_context = {
        'title': 'Логи',
        'description': 'Логи рассылок',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(mailing__owner=self.request.user)


class MailingLogView(LoginRequiredMixin, TemplateView):
    paginator = None
    permission_required = 'logger_app.view_mailing_log'
    template_name = 'logger_app/mailinglog_list.html'
    extra_context = {
        'title': 'Логи рассылки',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context_data['object_list'] = (MailingLog.objects.
                                           filter(mailing=self.kwargs.get('pk')).
                                           order_by('pk').reverse())
            context_data['title'] = Mailing.objects.get(pk=self.kwargs.get("pk"))
            context_data['description'] = f'Логи рассылки "{Mailing.objects.get(pk=self.kwargs.get("pk")).name}"'
        else:
            context_data['object_list'] = (MailingLog.objects.
                                           filter(mailing=self.kwargs.get('pk')).
                                           filter(mailing__owner=self.request.user).
                                           order_by('pk').reverse())
            mailing = Mailing.objects.filter(owner=self.request.user)
            context_data['title'] = get_object_or_404(mailing, pk=self.kwargs.get("pk"))
            context_data['description'] = f'Логи рассылки "{mailing.get(pk=self.kwargs.get("pk")).name}"'

        # Постраничная пагинация
        # В шаблоне для постраничной пагинации в FBV и TemplateView в цикле используется объект page_obj вместо object
        self.paginator = Paginator(context_data['object_list'], 10)
        page_number = self.request.GET.get('page')
        context_data['page_obj'] = self.paginator.get_page(page_number)

        return context_data
