from django.urls import path
from django.views.decorators.cache import cache_page

from main_app.apps import MainAppConfig
from main_app.views import IndexView, ContactView

app_name = MainAppConfig.name

urlpatterns = [
    path('', cache_page(60)(IndexView.as_view()), name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
]
