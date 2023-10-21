from django.contrib import admin

from service_app.models import Mailing, Periodicity


@admin.register(Periodicity)
class PeriodicityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'periodicity', 'title', 'start_time', 'stop_time', 'sending_time', 'status')
