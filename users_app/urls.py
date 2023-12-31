from django.urls import path

from users_app.apps import UsersAppConfig
from users_app.views import (LoginView, LogoutView, RegisterView, EmailVerifyView, PasswordRecoveryView, \
                             UpdateProfileView, UserListView, set_active, UserDetailView)

app_name = UsersAppConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email_verify/', EmailVerifyView.as_view(), name='email_verify'),
    path('password_recovery/', PasswordRecoveryView.as_view(), name='password_recovery'),
    path('user/list', UserListView.as_view(), name='list'),
    path('user/profile/<int:pk>/', UserDetailView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('user/active/<int:pk>/', set_active, name='set_active'),
]
