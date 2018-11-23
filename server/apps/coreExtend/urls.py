from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views

app_name="coreExtend"
urlpatterns = [
    path('login/password_reset/', auth_views.PasswordResetView.as_view(template_name='coreExtend/account/password_reset/form.html'), name='password_reset'),
    path('login/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='coreExtend/account/password_reset/done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='coreExtend/account/password_reset/confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='coreExtend/account/password_reset/complete.html'), name='password_reset_complete'),
    path('login/', auth_views.LoginView.as_view(template_name='coreExtend/login.html'), name='Login'),
    path('logout/', views.logout_user, name='Logout'),
    path('register/', views.register, name='Register'),
    path('account/password/', views.password, name='PasswordChange'),
    path('account/', views.EditAccount, name='AccountSettings'),
]
