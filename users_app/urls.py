from django.urls import path

from users_app.apps import UsersAppConfig
from users_app.views import LoginView, LogoutView, RegisterView, EmailVerifyView, PasswordRecoveryView, ProfileView

app_name = UsersAppConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email_verify/', EmailVerifyView.as_view(), name='email_verify'),
    path('password_recovery/', PasswordRecoveryView.as_view(), name='password_recovery'),
    path('profile', ProfileView.as_view(), name='profile'),
]