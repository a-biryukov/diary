from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', views.email_verification, name='email_confirm'),
    path('', cache_page(60)(views.UserLoginView.as_view(template_name='users/login.html')), name='login'),
    path('password-recovery/', views.PasswordRecoveryTemplateView.as_view(), name='password_recovery'),
    path('profile/<int:pk>/pass-change/', views.UserPasswordChangeView.as_view(
        template_name='users/password_change_form.html'),
        name='password_change'
    ),
    path('profile/<int:pk>', views.UserDetailView.as_view(), name='user_detail'),
    path('profile/<int:pk>/change/', views.UserUpdateView.as_view(), name='user_update'),
    path('profile/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('logout/', LogoutView.as_view(
        http_method_names=['post', 'get', 'options'],
        template_name='users/logout.html'),
        name='logout'
    ),
]
