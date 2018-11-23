from __future__ import absolute_import
from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from . import views

app_name="aggregator"
urlpatterns = [
    path('', views.Index, name='Index'),
    path('all/', views.AllFeedsListView.as_view(), name='AllFeeds'),
    path('tags/', views.FeedTagList, name = "FeedTagList"),
    path('tags/<slug:tag_name_slug>/', views.TagView, name ="FeedTagSingle"),
    path('search/', views.SearchListView.as_view(), name='Search'),
]
