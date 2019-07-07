
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

from .models import FeedItem, Feed, FeedList, FeedListThrough
from .forms import FeedModelForm

ITEM_COUNT = 6

def Index(request):
    feeds = []
    FeedQuery = Feed.objects.approved().filter(feedlist__slug='default').order_by('-group')

    for ft in FeedQuery:
        feeds.append((ft, ft.items()[0:ITEM_COUNT]))
    ctx = { 'object_list': feeds, 'title': 'jadedgamer.com',}
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
        context.update({'title': 'All Feeds | jadedgamer.com',})
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
    ctx = {'tags' : tags, 'alphabetized': result, 'title': 'Tags | jadedgamer.com',}
    template = 'aggregator/feed_tag_list.html'
    return render(request, template, ctx)

#Feeds by tag
def TagView(request, tag_name_slug):
    feeds = []
    tag = get_object_or_404(Tag, slug=tag_name_slug)
    for ft in Feed.objects.approved().filter(tags__name__in=[tag]).order_by('-title'):
        feeds.append((ft, ft.items()[0:ITEM_COUNT]))
    ctx = {'object_list': feeds, 'title': '{0} | jadedgamer.com'.format(tag) }
    return render(request, 'aggregator/feed_list.html', ctx)

@login_required
def AddFeed(request):
    #Lets users add new feeds to the aggregator.
    instance = Feed(owner=request.user)
    f = FeedModelForm(request.POST or None, instance=instance)
    if f.is_valid():
        f.save()
        messages.add_message(
            request, messages.INFO, 'Your feed has entered moderation. Please allow up to 1 week for review.')
        return redirect('aggregator:Index')

    ctx = {'form': f, 'adding': True, 'title': 'Submit A Feed | jadedgamer.com',}
    return render(request, 'aggregator/edit-feed.html', ctx)

@login_required
def EditFeed(request, feed_id):
    #Lets a user edit a feed they've previously added.
    feed = get_object_or_404(Feed, pk=feed_id, owner=request.user)
    f = FeedModelForm(request.POST or None, instance=feed)
    if f.is_valid():
        f.save()
        return redirect('aggregator:Index')

    ctx = {'form': f, 'feed': feed, 'adding': False, 'title': 'Edit Feed | jadedgamer.com',}
    return render(request, 'aggregator/edit-feed.html', ctx)


@login_required
def DeleteFeed(request, feed_id):
    #Lets a user delete a feed they've previously added.
    ## TODO: Make this a soft delete
    feed = get_object_or_404(Feed, pk=feed_id, owner=request.user)
    if request.method == 'POST':
        feed.delete()
        return redirect('aggregator:Index')
    return render(request, 'aggregator/delete-confirm.html', {'feed': feed, 'title': 'Delete Feed | jadedgamer.com',})

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

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context.update({'title': 'Search | jadedgamer.com',})
        return context
