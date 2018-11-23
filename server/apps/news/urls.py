from __future__ import absolute_import
from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from . import views

app_name="news"
urlpatterns = [
    path('', views.NewsList.as_view(), name='NewsLatest'),
]
