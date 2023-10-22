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
    fields = ['name', 'message', 'periodic', 'start_time', 'stop_time', 'customers',]
    extra_context = {
        'title': 'Рассылки',
        'description': 'Создание новой рассылки',
    }


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['name', 'message', 'periodic', 'start_time', 'stop_time', 'customers',]
    success_url = reverse_lazy('service_app:index')
    extra_context = {
        'title': 'Рассылки',
        'description': 'Изменение рассылки',
    }

    def post(self, request, *args, **kwargs):
        Mailing.objects.update(status=Mailing.CREATED)
        print(request.POST)
        return super().post(request, *args, **kwargs)


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('service_app:index')
    extra_context = {
        'description': 'Удаление рассылки',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = get_object_or_404(Mailing, pk=self.kwargs.get('pk'))
        return context_data


def toggle_activity(request, pk):
    item = get_object_or_404(Mailing, pk=pk)
    if item.status == Mailing.PAUSED:
        item.status = Mailing.CREATED
    else:
        item.status = Mailing.PAUSED

    item.save()

    return redirect(reverse('service_app:index'))


def start_mailing(request, pk):
    send_mailing(Mailing.objects.get(pk=pk), manual=True)
    return redirect(reverse('service_app:index'))
