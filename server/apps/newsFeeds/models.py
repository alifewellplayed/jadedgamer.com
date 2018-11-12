
import uuid

from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from taggit.managers import TaggableManager

from util.slug import unique_slugify
from .managers import FeedManager, FeedItemManager

import logging
logger = logging.getLogger('default')

STATUS_CHOICES = (
    (1, 'Pending'),
    (2, 'Denied'),
    (3, 'Approved'),
)

FEED_TYPE = (
    (1, 'RSS'),
    (2, 'JSON'),
    (3, 'Twitter'),
)

FEEDLIST_CHOICES = (
    (True, 'Only me'),
    (False, 'Everyone')
)

class FeedList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    can_self_add = models.BooleanField(help_text=_("Who can see this list?"), choices=FEEDLIST_CHOICES, default=False)
    date_added = models.DateTimeField(verbose_name=_("When list was added to the site"), auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lists', blank=True, null=True )
    feeds = models.ManyToManyField('Feed', blank=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/lists/%s/" % (self.id)

    def items(self):
        feeds = list(self.feeds.all())
        return FeedItem.objects.active().filter(feed__in=feeds)[:25]

    def save(self, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)
        super(FeedList, self).save(**kwargs)

    class Meta:
        ordering = ("-date_added",)

class Feed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, blank=True)
    site_url = models.URLField(unique=True, max_length=500, blank=True)
    feed_url = models.URLField(unique=True, max_length=500)
    active = models.BooleanField(default=True, db_index=True)
    feed_type = models.IntegerField(max_length=1, choices=FEED_TYPE, default=1)
    approval_status = models.IntegerField(max_length=1, choices=STATUS_CHOICES, default=1)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='feeds')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    next_scheduled_update = models.DateTimeField()
    last_story_date = models.DateTimeField(null=True, blank=True)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True,)
    num_subscribers = models.IntegerField(default=-1)
    has_feed_exception = models.BooleanField(default=False, db_index=True)
    has_page_exception = models.BooleanField(default=False, db_index=True)
    favicon_color = models.CharField(max_length=6, null=True, blank=True)
    favicon_not_found = models.BooleanField(default=False)
    search_indexed = models.NullBooleanField(default=None, null=True, blank=True)
    tags = TaggableManager()
    objects = FeedManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/sites/%s/" % (self.slug,)

    def items(self):
        return FeedItem.objects.active().filter(feed=self)[:10]

    def item_count(self):
        item_counts = FeedItem.objects.filter(feed=self).count()
        return item_counts

    def save(self, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Feed, self).save(**kwargs)
        if settings.SUPERFEEDR_CREDS != None and self.approval_status == APPROVED_FEED:
            Subscription.objects.subscribe(self.feed_url, settings.PUSH_HUB)

    def delete(self, **kwargs):
        super(Feed, self).delete(**kwargs)
        if settings.SUPERFEEDR_CREDS is not None:
            self.unsubscribe()

    def unsubscribe(self):
        try:
            Subscription.objects.get(topic=self.feed_url).unsubscribe()
        except Subscription.DoesNotExist:
            pass

    class Meta:
        ordering = ("title",)

class FeedItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.CharField(max_length=500, db_index=True)
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=500)
    original_title = models.CharField(max_length=500)
    link = models.URLField(max_length=500)
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = FeedItemManager()

    def clicks(self):
        points = FeedItem.objects.filter(linkclick__link=self)
        return points.count()

    class Meta:
        ordering = ("-date_added",)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/item/%s/" % (self.id)
