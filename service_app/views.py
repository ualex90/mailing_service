from django.shortcuts import render
from django.views.generic import ListView

from service_app.models import Mailing


class MailingListView(ListView):
    model = Mailing
    template_name = 'service_app/index.html'
