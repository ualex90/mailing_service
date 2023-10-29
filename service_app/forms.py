from django import forms
from django.forms import CheckboxInput

from service_app.models import Mailing, Message


class StyleFrmMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFrmMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ['name', 'message', 'periodic', 'start_time', 'stop_time', 'customers',]


class MessageForm(StyleFrmMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = ['title', 'body',]
