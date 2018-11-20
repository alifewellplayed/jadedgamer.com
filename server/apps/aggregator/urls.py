from __future__ import absolute_import
from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from . import views

app_name="aggregator"
urlpatterns = [
    path('', views.Index, name='index'),
    path('all/', views.AllFeedsListView.as_view(), name='AllFeeds'),
    path('search/', views.SearchListView.as_view(), name='Search'),
]
