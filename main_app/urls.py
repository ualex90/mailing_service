from django.urls import path

from main_app.apps import MainAppConfig
from main_app.views import IndexView

app_name = MainAppConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
