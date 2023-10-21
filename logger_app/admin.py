from django.contrib import admin

from logger_app.models import MailingLog


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_attempt', 'mailing', 'server_response', 'is_successfully',)
