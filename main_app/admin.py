from django.contrib import admin

from main_app.models import Contact, Message


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'inn', 'address', 'phone')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'message')
    # фильтрация
    list_filter = ('name', 'phone', 'email',)
    # поиск
    search_fields = ('name', 'phone', 'email', 'message')