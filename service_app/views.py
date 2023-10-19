from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from service_app.models import Mailing


class MailingListView(ListView):
    model = Mailing
    queryset = Mailing.objects.filter().order_by('pk').reverse()
    template_name = 'service_app/index.html'

    extra_context = {
        'title': 'Рассылки',
        'description': 'Список рассылок',
    }


class MailingCreateView(CreateView):
    model = Mailing
    success_url = reverse_lazy('service_app:index')
    fields = ['name', 'title', 'body', 'periodicity', 'mailing_time', 'status', 'is_active',]
    extra_context = {
        'title': 'Рассылки',
        'description': 'Создание новой рассылки',
    }


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['name', 'title', 'body', 'periodicity', 'mailing_time', 'status', 'is_active', ]
    success_url = reverse_lazy('service_app:index')
    extra_context = {
        'title': 'Рассылки',
        'description': 'Изменение рассылки',
    }


def toggle_activity(request, pk):
    item = get_object_or_404(Mailing, pk=pk)
    if item.is_active:
        item.is_active = False
    else:
        item.is_active = True

    item.save()

    return redirect(reverse('service_app:index'))
