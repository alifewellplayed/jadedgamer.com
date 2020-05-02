from rest_framework import generics, permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from api.serializers import NewsItemSerializer
from .models import NewsItem, NewsItemInstance

import logging
logger = logging.getLogger('default')

@permission_classes((AllowAny, ))
class LatestView(APIView):
  def get(self, request, format=None):
    queryset = NewsItem.objects.public()
    serializer = NewsItemSerializer(queryset, many=True)
    return Response({
        'data': serializer.data,
    })

@permission_classes((AllowAny, ))
class PopularView(APIView):
  def get(self, request, format=None):
    queryset = NewsItem.objects.public()
    serializer = NewsItemSerializer(queryset, many=True)
    return Response({
        'data': serializer.data,
    })