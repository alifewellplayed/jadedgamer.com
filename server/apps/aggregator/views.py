
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

from .models import FeedItem, Feed, FeedList
from .forms import FeedModelForm

def Index(request):
    feeds = []
    FeedQuery = Feed.objects.approved().order_by('title')
    for ft in FeedQuery:
        feeds.append((ft, ft.items()[0:ITEM_COUNT]))
    ctx = {
        'object_list': feeds,
        'headers': False,
    }
    tpl = 'aggregator/index.html'
    return render(request, tpl, ctx)
