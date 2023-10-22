from django.contrib import admin

from service_app.models import Mailing, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'periodic', 'start_time', 'stop_time', 'status')
