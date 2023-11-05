from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from customers_app.forms import CustomerForm
from customers_app.models import Customer


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    queryset = Customer.objects.filter().order_by('pk').reverse()
    extra_context = {
        'title': 'Клиенты',
        'description': 'Список клиентов',
    }


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    extra_context = {
        'description': 'Карточка клиента',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        post_item = Customer.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'{post_item.last_name}, {post_item.first_name}, {post_item.surname}'
        return context_data


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customers_app:list')
    extra_context = {
        'title': 'Клиент',
        'description': 'Добавить клиента',
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
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


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
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
