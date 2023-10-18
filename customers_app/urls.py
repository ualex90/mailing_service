from django.urls import path

from customers_app.apps import CustomersAppConfig

app_name = CustomersAppConfig.name

urlpatterns = [
    # path('list', ..., name='list'),
    # path('customer/<int:pk>', ..., name='customer'),
]
