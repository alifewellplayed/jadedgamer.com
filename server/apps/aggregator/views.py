
import json
import datetime

from collections import OrderedDict

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.decorators.cache import cache_page
from django.db.models import Count
from django.core.cache import cache
from taggit.models import Tag
from redirect.models import LinkClick
#from threadedcomments.models import ThreadedComment

from .models import FeedItem, Feed, FeedList
from .forms import FeedModelForm

ITEM_COUNT = 5

def Index(request):
    feeds = []
    FeedQuery = Feed.objects.approved().order_by('title')
    for ft in FeedQuery:
        feeds.append((ft, ft.items()[0:ITEM_COUNT]))
    ctx = { 'object_list': feeds, 'title': 'Home', }
    tpl = 'aggregator/feed_list.html'
    return render(request, tpl, ctx)

#All Published feeds
class AllFeedsListView(ListView):
    paginate_by = 15
    template_name = 'aggregator/feed_list.html'

    def get_queryset(self):
        feeds = []
        for ft in Feed.objects.approved().order_by('title'):
            feeds.append((ft, ft.items()[0:ITEM_COUNT]))
        return feeds

    def get_context_data(self, **kwargs):
        context = super(AllFeedsListView, self).get_context_data(**kwargs)
        context.update({'title': 'All Feeds',})
        return context

#List of all tags
def FeedTagList(request):
    tags = Tag.objects.order_by('name')
    result = OrderedDict()
    # first separate by letter
    for tag in tags:
        letter = tag.name[0]
        if letter in result.keys():
            result[letter].append(tag)
        else:
            result[letter] = [tag]
    # then alphabetize each letter's list
    for letter, val in result.items():
        val.sort(key=lambda x: x.name)
    ctx = {'tags' : tags, 'alphabetized': result}
    template = 'aggregator/feed_tag_list.html'
    return render(request, template, ctx)

#Feeds by tag
def TagView(request, tag_name_slug):
    feeds = []
    tag = get_object_or_404(Tag, slug=tag_name_slug)
    for ft in Feed.objects.approved().filter(tags__name__in=[tag]).order_by('-title'):
        feeds.append((ft, ft.items()[0:ITEM_COUNT]))
    ctx = {'object_list': feeds, 'title': tag }
    return render(request, 'aggregator/feed_list.html', ctx)

class SearchListView(ListView):
    model = FeedItem
    paginate_by = 15
    template_name = 'aggregator/search.html'

    def get_queryset(self):
        qs = FeedItem.objects.all()
        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            title_vector = SearchVector('title', weight='A')
            content_vector = SearchVector('summary', weight='B')
            vectors = title_vector + content_vector
            qs = qs.annotate(search=vectors).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vectors, query)).order_by('-rank')
        return qs
