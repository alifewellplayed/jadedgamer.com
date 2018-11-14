
import json
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import SortedDict
from django.views.generic.list import ListView
from django.views.decorators.cache import cache_page
from django.db.models import Count
from django.core.cache import cache
from taggit.models import Tag
from newsRedirect.models import LinkClick
from voting.models import Vote
from threadedcomments.models import ThreadedComment

from newsFeeds.models import FeedItem, Feed, FeedList, APPROVED_FEED, PENDING_FEED, DENIED_FEED
from newsFeeds.forms import FeedModelForm, FeedListModelForm

def Index(request):
    feeds = []
    if request.user.is_authenticated():
        FeedQuery = Feed.objects.approved().filter(subscribers=request.user).order_by('title')
    else:
        FeedQuery = Feed.objects.approved().filter(feedlist__title='Default').order_by('title')
    for ft in FeedQuery:
        feeds.append((ft, ft.items()[0:ITEM_COUNT]))
    ctx = {'object_list': feeds, 'headers': False,}
    tpl = 'newsFeed/index.html'
    return render(request, tpl, ctx)
