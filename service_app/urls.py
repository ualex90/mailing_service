from django.urls import path

from service_app.apps import ServiceAppConfig
from service_app.views import MailingListView, MailingCreateView, MailingUpdateView, toggle_activity

app_name = ServiceAppConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='index'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='update'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]
