from django.urls import path

from service_app.apps import ServiceAppConfig
from service_app.views import MailingListView, MailingCreateView, MailingUpdateView, toggle_activity,  \
    MailingDeleteView, start_mailing

app_name = ServiceAppConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='index'),
    path('mailing/create/', MailingCreateView.as_view(), name='create'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='update'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),
    path('mailing/activity/<int:pk>/', toggle_activity, name='toggle_activity'),
    path('mailing/send/<int:pk>/', start_mailing, name='start_mailing'),
]
