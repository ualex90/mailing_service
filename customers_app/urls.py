from django.urls import path

from customers_app.apps import CustomersAppConfig
from customers_app.views import CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView, \
    CustomerDeleteView

app_name = CustomersAppConfig.name

urlpatterns = [
    path('list/', CustomerListView.as_view(), name='list'),
    path('customer/<int:pk>', CustomerDetailView.as_view(), name='detail'),
    path('create/', CustomerCreateView.as_view(), name='create'),
    path('update/<int:pk>', CustomerUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', CustomerDeleteView.as_view(), name='delete'),
]
