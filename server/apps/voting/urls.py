from django.conf.urls import url
from rest_framework_nested import routers

from .views import FeedItemVote, FeedItemUnvote

app_name = 'Voting'
urlpatterns = [
    url(r'^item/(?P<pk>[0-9]+)/vote/$', FeedItemVote.as_view(), name='vote'),
    url(r'^item/(?P<pk>[0-9]+)/unvote/$', FeedItemUnvote.as_view(), name='unvote'),
]
