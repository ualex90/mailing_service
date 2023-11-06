from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from service_app.forms import MessageForm, MailingForm
from service_app.models import Mailing, Message
from service_app.services import send_mailing


class UserHasPermissionMixin:
    def has_permission(self):
        # Проверяем, является ли пользователь владельцем рассылки, если да, то разрешаем операцию
        if self.model.objects.get(pk=self.kwargs.get('pk')).owner == self.request.user:
            return True
        # если не является, то следуем ограничениям прав permission_required
        return super().has_permission()


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    queryset = Mailing.objects.filter().order_by('pk').reverse()
    template_name = 'service_app/index.html'

    extra_context = {
        'title': 'Рассылки',
        'description': 'Список рассылок',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    queryset = Message.objects.filter().order_by('pk').reverse()

    extra_context = {
        'title': 'Сообщения',
        'description': 'Список сообщений',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    success_url = reverse_lazy('service_app:index')
    form_class = MailingForm
    extra_context = {
        'title': 'Рассылки',
        'description': 'Создание новой рассылки',
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Добавляем в форму аргумент содержащий текущего пользователя
        kwargs["user"] = self.request.user
        return kwargs

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


class MailingUpdateView(LoginRequiredMixin, UserHasPermissionMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    permission_required = 'service_app.change_mailing'
    form_class = MailingForm
    success_url = reverse_lazy('service_app:index')
    extra_context = {
        'title': 'Рассылки',
        'description': 'Изменение рассылки',
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Добавляем в форму аргумент содержащий текущего пользователя
        kwargs["user"] = self.request.user
        return kwargs


class MessageUpdateView(LoginRequiredMixin, UserHasPermissionMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    permission_required = 'service_app.change_message'
    success_url = reverse_lazy('service_app:message_list')
    form_class = MessageForm
    extra_context = {
        'title': 'Сообщение',
        'description': 'Изменение сообщения',
    }


class MailingDeleteView(LoginRequiredMixin, UserHasPermissionMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    permission_required = 'service_app.delete_mailing'
    success_url = reverse_lazy('service_app:index')
    extra_context = {
        'description': 'Удаление рассылки',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = get_object_or_404(Mailing, pk=self.kwargs.get('pk'))
        return context_data


class MessageDeleteView(LoginRequiredMixin, UserHasPermissionMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    permission_required = 'service_app.delete_message'
    success_url = reverse_lazy('service_app:message_list')
    extra_context = {
        'description': 'Удаление сообщения',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = get_object_or_404(Message, pk=self.kwargs.get('pk'))
        return context_data


@login_required
def set_pause(request, pk):
    item = get_object_or_404(Mailing, pk=pk)

    # Проверяем, является ли пользователь создателем рассылки или есть ли у него права на постановку паузы
    if item.owner == request.user or request.user.has_perms(['service_app.set_pause']):
        if item.status == Mailing.PAUSED:
            item.status = Mailing.CREATED
        else:
            item.status = Mailing.PAUSED

        item.save()

    return redirect(reverse('service_app:index'))


@login_required
def start_mailing(request, pk):
    item = get_object_or_404(Mailing, pk=pk)
    if item.owner == request.user or request.user.has_perms(['service_app.set_pause']):
        send_mailing(item, manual=True)
    return redirect(reverse('service_app:index'))


@permission_required('set_active')
@login_required
def set_active(request, pk):
    item = get_object_or_404(Mailing, pk=pk)
    if item.owner == request.user or request.user.is_staff:
        if item.status == Mailing.PAUSED:
            item.status = Mailing.CREATED
        else:
            item.status = Mailing.PAUSED

        item.save()

    return redirect(reverse('service_app:index'))
