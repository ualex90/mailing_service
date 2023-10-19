from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from customers_app.models import Customer


class CustomerListView(ListView):
    model = Customer
    queryset = Customer.objects.filter().order_by('pk').reverse()
    extra_context = {
        'title': 'Клиенты',
        'description': 'Список клиентов',
    }


class CustomerDetailView(DetailView):
    model = Customer
    extra_context = {
        'description': 'Карточка клиента',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        post_item = Customer.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'{post_item.last_name}, {post_item.first_name}, {post_item.surname}'
        return context_data


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['last_name', 'first_name', 'surname', 'email', 'comment', 'subscriptions',]
    success_url = reverse_lazy('customers_app:list')
    extra_context = {
        'title': 'Клиент',
        'description': 'Добавить клиента',
    }


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['last_name', 'first_name', 'surname', 'email', 'comment', 'subscriptions',]
    extra_context = {
        'description': 'Изменить клиента',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        post_item = Customer.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'{post_item.last_name}, {post_item.first_name}, {post_item.surname}'
        return context_data

    def get_success_url(self):
        return reverse('customers_app:detail', args=[self.object.pk])


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers_app:list')
    extra_context = {
        'description': 'Удаление клиента',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        item = Customer.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'{item.last_name}, {item.first_name}, {item.surname}'
        return context_data
