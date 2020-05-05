
from rest_framework import filters
import json
from collections import OrderedDict
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from taggit.models import Tag
from redirect.models import LinkClick
from rest_framework import generics, permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import filters

from api.serializers import FeedSerializer, FeedItemSerializer
from .models import FeedItem, Feed, FeedList, FeedListThrough
from .forms import FeedModelForm

#Index
@permission_classes((AllowAny, ))
class DefaultListView(APIView):
  def get(self, request, format=None):
    queryset = Feed.objects.approved().filter(feedlist__slug='default').order_by('-group')
    serializer = FeedSerializer(queryset, many=True)
    return Response({
      'feeds': serializer.data,
    })

#All Published feeds
@permission_classes((AllowAny, ))
class AllFeedsListView(APIView):
  def get(self, request, format=None):
    queryset = Feed.objects.approved().order_by('-group')
    serializer = FeedSerializer(queryset, many=True)
    return Response({
      'feeds': serializer.data,
    })

@permission_classes((AllowAny, ))
class FeedItemAPIView(generics.ListCreateAPIView):
    search_fields = ['title', 'summary', 'description']
    filter_backends = (filters.SearchFilter,)
    queryset = FeedItem.objects.all()
    serializer_class = FeedItemSerializer

#List of all tags
@permission_classes((AllowAny, ))
class AllTagsView(APIView):
  def get(self, request, format=None):
    tags = Tag.objects.order_by('name')
    result = OrderedDict()
    for tag in tags:
        letter = tag.name[0]
        if letter in result.keys():
            result[letter].append(tag)
        else:
            result[letter] = [tag]
    for letter, val in result.items():
        val.sort(key=lambda x: x.name)
    return Response({
        'tags': tags,
        'alphabetized': result,
    })

#Feeds by tag
@permission_classes((AllowAny, ))
class FeedsByTag(APIView):
    def get_object(self, tag_name_slug):
        try:
            tag = get_object_or_404(Tag, slug=tag_name_slug)
            if tag:
                qs = Feed.objects.approved().filter(tags__name__in=[tag]).order_by('-title')
            return qs
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, tag_name_slug, format=None):
        data = self.get_object(tag_name_slug=tag_name_slug)
        return Response({
            'data': data
        })
