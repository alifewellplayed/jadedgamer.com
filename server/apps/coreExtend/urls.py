from django.conf.urls import *
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from .forms import PasswordResetForm
from . import views

app_name="coreExtend"

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(
        template_name='coreExtend/login.html',
        extra_context={'account_settings': True,}),
        name='login'
    ),
    url(r'^logout/$', views.logout_user, name='Logout'),
    url(r'^register/$', views.register, name='Register'),
    url(r'^account/password/$', views.password, name='password_change'),
    url(r'^account/$', views.EditAccount, name='AccountSettings'),
]
