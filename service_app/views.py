from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from service_app.forms import MessageForm, MailingForm
from service_app.models import Mailing, Message
from service_app.services import send_mailing


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    queryset = Mailing.objects.filter().order_by('pk').reverse()
    template_name = 'service_app/index.html'

    extra_context = {
        'title': 'Рассылки',
        'description': 'Список рассылок',
    }


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    queryset = Message.objects.filter().order_by('pk').reverse()

    extra_context = {
        'title': 'Сообщения',
        'description': 'Список сообщений',
    }


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    success_url = reverse_lazy('service_app:index')
    form_class = MailingForm
    extra_context = {
        'title': 'Рассылки',
        'description': 'Создание новой рассылки',
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    success_url = reverse_lazy('service_app:message_list')
    form_class = MessageForm
    extra_context = {
        'title': 'Сообщение',
        'description': 'Создание нового сообщения',
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('service_app:index')
    extra_context = {
        'title': 'Рассылки',
        'description': 'Изменение рассылки',
    }


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    success_url = reverse_lazy('service_app:message_list')
    form_class = MessageForm
    extra_context = {
        'title': 'Сообщение',
        'description': 'Изменение сообщения',
    }


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('service_app:index')
    extra_context = {
        'description': 'Удаление рассылки',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = get_object_or_404(Mailing, pk=self.kwargs.get('pk'))
        return context_data


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('service_app:message_list')
    extra_context = {
        'description': 'Удаление сообщения',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = get_object_or_404(Message, pk=self.kwargs.get('pk'))
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
