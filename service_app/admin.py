from django.contrib import admin

from service_app.models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'periodicity', 'mailing_time', 'status')
