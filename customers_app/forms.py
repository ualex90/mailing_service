from django import forms

from customers_app.models import Customer
from service_app.forms import StyleFrmMixin


class CustomerForm(StyleFrmMixin, forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['last_name', 'first_name', 'surname', 'email', 'comment', 'is_mailing']
