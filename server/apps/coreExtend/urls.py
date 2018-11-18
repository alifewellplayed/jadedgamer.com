from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from .forms import PasswordResetForm
from . import views

app_name="coreExtend"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='coreExtend/login.html'), name='Login'),
    path('logout/', views.logout_user, name='Logout'),
    path('register/', views.register, name='Register'),
    path('account/password/', views.password, name='PasswordChange'),
    path('account/', views.EditAccount, name='AccountSettings'),
]
