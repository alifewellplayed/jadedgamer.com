from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.http import Http404
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from rest_framework import generics, permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from aggregator.models import FeedList, Feed
from api.serializers import FeedSerializer, UserSerializer

import logging
logger = logging.getLogger('default')


@permission_classes((AllowAny, ))
class HomeView(APIView):
  def get(self, request, format=None):
    queryset = Feed.objects.approved().filter(feedlist__slug='default').order_by('-group')
    serializer = FeedSerializer(queryset, many=True)
    return Response({
      'feeds': serializer.data,
    })

class current_user(APIView):
  def get_object(self):
    try:
      return User.objects.get(pk=self.request.user.id)
    except User.DoesNotExist:
      raise Http404

  def get(self, request, format=None):
    user_serializer = UserSerializer(request.user)
    return Response({
      'user': user_serializer.data,
    })
