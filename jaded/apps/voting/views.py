from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from aggregator.models import Feed, FeedItem


class FeedItemVotingView(generics.UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsNotBlacklisted)

    def perform_action(self, user_id, item):
        raise NotImplementedError()

    def update(self, request, pk=None, *args, **kwargs):
        item = get_object_or_404(FeedItem, id=pk)
        self.check_object_permissions(request, item)
        self.perform_action(request.user.id, item)
        return Response({"num_vote_up": item.votes.count()}, status=status.HTTP_200_OK)


class FeedItemVote(FeedItemVotingView):
    def perform_action(self, user_id, item):
        item.votes.up(user_id)


class FeedItemUnvote(FeedItemVotingView):
    def perform_action(self, user_id, item):
        item.votes.delete(user_id)
