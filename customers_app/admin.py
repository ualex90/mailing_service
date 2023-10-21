from django.contrib import admin

from customers_app.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_name', 'first_name', 'surname', 'email', 'is_mailing',)
