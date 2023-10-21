from django.urls import path

from logger_app.apps import LoggerAppConfig
from logger_app.views import MailingLogListView, MailingLogView

app_name = LoggerAppConfig.name

urlpatterns = [
    path('mailing/', MailingLogListView.as_view(), name='log'),
    path('mailing/<int:pk>', MailingLogView.as_view(), name='mailing_log'),
]
