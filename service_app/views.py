from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from service_app.models import Mailing
from service_app.services import send_mailing


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
    fields = ['name', 'title', 'body', 'periodicity', 'start_time', 'stop_time', 'status', 'is_active',]
    extra_context = {
        'title': 'Рассылки',
        'description': 'Создание новой рассылки',
    }


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['name', 'title', 'body', 'periodicity', 'start_time', 'stop_time', 'status', 'is_active', ]
    success_url = reverse_lazy('service_app:index')
    extra_context = {
        'title': 'Рассылки',
        'description': 'Изменение рассылки',
    }


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('customers_app:list')
    extra_context = {
        'description': 'Удаление рассылки',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = get_object_or_404(Mailing, pk=self.kwargs.get('pk'))
        return context_data


def toggle_activity(request, pk):
    item = get_object_or_404(Mailing, pk=pk)
    if item.is_active:
        item.is_active = False
    else:
        item.is_active = True

    item.save()

    return redirect(reverse('service_app:index'))


def start_mailing(request, pk):
    send_mailing(pk)
    return redirect(reverse('service_app:index'))
