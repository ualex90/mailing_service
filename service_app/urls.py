from django.urls import path

from service_app.apps import ServiceAppConfig
from service_app.views import MailingListView, MailingCreateView, MailingUpdateView, set_pause, \
    MailingDeleteView, start_mailing, MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    set_active

app_name = ServiceAppConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='index'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/activity/<int:pk>/', set_pause, name='pause'),
    path('mailing/send/<int:pk>/', start_mailing, name='start_mailing'),
    path('mailing/active/<int:pk>/', set_active, name='set_active'),
    path('message/list/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]
