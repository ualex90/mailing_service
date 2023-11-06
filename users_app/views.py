from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView

import users_app
from users_app.forms import LoginForm, RegisterForm, UserProfileForm
from users_app.models import User
from users_app.utils import get_user_key, get_password


class LoginView(BaseLoginView):
    template_name = 'users_app/login.html'
    form_class = LoginForm


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users_app/register.html'
    success_url = reverse_lazy('users_app:email_verify')

    def form_valid(self, form):
        key = get_user_key()
        self.object = form.save()
        self.object.key = key
        self.object.save()
        send_mail(
            subject='подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке: '
                    f'http://127.0.0.1:8000/users/email_verify/?key={key}',
            from_email=None,
            recipient_list=[self.object.email],
        )
        return super().form_valid(form)


class EmailVerifyView(TemplateView):
    template_name = 'users_app/user_verification.html'
    extra_context = {
        'title': 'Подтверждение регистрации',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key = self.request.GET.get('key')

        # Если в запросе есть 'key', то выполняем верификацию
        if key:
            try:
                user = User.objects.get(key=key)
            except users_app.models.User.DoesNotExist:
                context['description'] = 'Пользователь не существует'
            else:
                user.is_active = True
                user.save()
                context['description'] = 'Спасибо за успешную регистрацию!'
                context['verify'] = True
            finally:
                return context

        # Если нет ключа, то предложим пользователю заглянуть в свою почту
        context['description'] = 'Для подтверждения регистрации перейдите по ссылке отправленной на Ваш email'
        context['register_end'] = True
        return context


class PasswordRecoveryView(TemplateView):
    template_name = 'users_app/reset_password.html'
    extra_context = {
        'title': 'Восстановление пароля',
    }

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        email = self.request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except users_app.models.User.DoesNotExist:
            context['description'] = 'Неверный email. Попробуйте еще раз'
        else:
            password = get_password()
            user.set_password(password)
            user.save()
            send_mail(
                subject='Восстановление пароля',
                message=f'Ваш новый пароль: {password}',
                from_email=None,
                recipient_list=[email],
            )

            return redirect(reverse('users_app:login'))
        return self.render_to_response(context)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    queryset = model.objects.filter().order_by('pk').reverse()
    permission_required = 'users_app.view_user'
    extra_context = {
        'title': 'Пользователи',
        'description': 'Список пользователей',
    }


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = User
    permission_required = 'users_app.view_user'
    extra_context = {
        'title': 'Пользователь',
        'description': 'Данные пользователя',
    }


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users_app:profile')
    extra_context = {
        'title': 'Профиль',
        'description': 'Редактировать профиль пользователя',
    }

    def get_object(self, queryset=None):
        return self.request.user


@permission_required('users_app.set_active')
@login_required
def set_active(request, pk):
    item = get_object_or_404(User, pk=pk)

    # Суперпользователя может заблокировать или разблокировать только суперпользователь
    if not item.is_superuser or request.user.is_superuser:
        if item.is_active:
            item.is_active = False
        else:
            item.is_active = True

        item.save()

    return redirect(reverse('users_app:list'))
