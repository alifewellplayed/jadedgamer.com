from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from . import views

app_name = "redirect"
urlpatterns = [
    path("<slug:slug>/", views.LinkRedirect, name="link_redirect"),
]
