from django.urls import path

from service_app.apps import ServiceAppConfig


app_name = ServiceAppConfig.name

urlpatterns = [
    # path('mailing/list/', ..., name='list'),
]
