from django.urls import path

from service_app.apps import ServiceAppConfig
from service_app.views import MailingListView

app_name = ServiceAppConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='index'),
]
