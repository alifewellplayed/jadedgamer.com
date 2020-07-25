from __future__ import absolute_import
from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from . import views

app_name = "aggregator"
urlpatterns = [
    path("", views.Index, name="Index"),
    path("feeds/all/", views.AllFeedsListView.as_view(), name="AllFeeds"),
    path("feeds/submit/", views.AddFeed, name="AddFeed"),
    path("feeds/edit/<int:feed_id>/", views.EditFeed, name="EditFeed"),
    path("feeds/delete/<int:feed_id>", views.DeleteFeed, name="DeleteFeed"),
    path("feeds/tags/", views.FeedTagList, name="FeedTagList"),
    path("feeds/tags/<slug:tag_name_slug>/", views.TagView, name="FeedTagSingle"),
    path("search/", views.SearchListView.as_view(), name="Search"),
]
