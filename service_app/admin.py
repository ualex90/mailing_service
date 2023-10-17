from django.contrib import admin

from service_app.models import Mailing, Log


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'periodicity', 'mailing_time', 'status')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing', 'last_attempt', 'attempt_status', 'server_response')
