from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from service_app.forms import StyleFrmMixin
from users_app.models import User


class LoginForm(StyleFrmMixin, AuthenticationForm):
    pass


class RegisterForm(StyleFrmMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserProfileForm(StyleFrmMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'country', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
