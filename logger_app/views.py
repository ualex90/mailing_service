from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import OuterRef
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from logger_app.models import MailingLog
from service_app.models import Mailing
from service_app.views import UserHasPermissionMixin


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog
    queryset = MailingLog.objects.filter().order_by('pk').reverse()
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
        else:
            context_data['object_list'] = (MailingLog.objects.
                                           filter(mailing=self.kwargs.get('pk')).
                                           filter(mailing__owner=self.request.user).
                                           order_by('pk').reverse())
        context_data['title'] = Mailing.objects.get(pk=self.kwargs.get("pk"))
        context_data['description'] = f'Логи рассылки "{Mailing.objects.get(pk=self.kwargs.get("pk")).name}"'
        return context_data
