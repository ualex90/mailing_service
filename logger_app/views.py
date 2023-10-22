from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from logger_app.models import MailingLog
from service_app.models import Mailing
from django.core.paginator import Paginator


class MailingLogListView(ListView):
    model = MailingLog
    queryset = MailingLog.objects.filter().order_by('pk').reverse()
    # paginate_by = 9
    extra_context = {
        'title': 'Логи',
        'description': 'Логи рассылок',
    }


class MailingLogView(TemplateView):
    template_name = 'logger_app/mailinglog_list.html'
    extra_context = {
        'title': 'Логи рассылки',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = MailingLog.objects.filter(mailing=self.kwargs.get('pk')).order_by('pk').reverse()
        context_data['title'] = Mailing.objects.get(pk=self.kwargs.get("pk"))
        context_data['description'] = f'Логи рассылки "{Mailing.objects.get(pk=self.kwargs.get("pk")).name}"'
        return context_data
