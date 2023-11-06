from django import forms
from django.contrib import auth
from django.forms import CheckboxInput

from customers_app.models import Customer
from service_app.models import Mailing, Message


class StyleFrmMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFrmMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # получаем пользователя и с целью избежания ошибок, удаляем
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # фильтруем сообщения и клиентов по пользователю если он не является персоналом
        if not self.user.is_staff:
            self.fields['message'].queryset = Message.objects.filter(owner=self.user)
            self.fields['customers'].queryset = Customer.objects.filter(owner=self.user)

    class Meta:
        model = Mailing
        fields = ['name', 'message', 'periodic', 'start_time', 'stop_time', 'customers',]


class MessageForm(StyleFrmMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = ['title', 'body',]
