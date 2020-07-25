import uuid

from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from django_push.subscriber import signals as push_signals
from django_push.subscriber.models import Subscription
from coreExtend.util.slug import unique_slugify
from coreExtend.models import UUIDTaggedItem

from .managers import FeedManager, FeedItemManager, FeedListManager

import logging

logger = logging.getLogger("default")

STATUS_CHOICES = (
    (1, "Pending"),
    (2, "Denied"),
    (3, "Approved"),
    (4, "Deleted"),
)

FEED_TYPE = (
    (1, "RSS"),
    (2, "JSON"),
    (3, "Twitter"),
)

FEED_DISPLAY = (
    (0, "default"),
    (1, "Display Thumbnails"),
)

FEEDLIST_CHOICES = ((True, "Only me"), (False, "Everyone"))


class FeedList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    can_self_add = models.BooleanField(help_text="Who can edit this list?", choices=FEEDLIST_CHOICES, default=True)
    date_added = models.DateTimeField(verbose_name="When list was added to the site", auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="lists", blank=True, null=True, on_delete=models.SET_NULL
    )
    feeds = models.ManyToManyField("Feed", through="FeedListThrough", blank=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    objects = FeedListManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/lists/%s/" % (self.id)

    def feeds_ordered(self):
        return [f.feed for f in FeedListThrough.objects.filter(feedlist=self).order_by("order")]

    def items(self):
        feeds = list(self.feeds.all())
        return FeedItem.objects.active().filter(feed__in=feeds)[:25]

    def save(self, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)
        super(FeedList, self).save(**kwargs)

    class Meta:
        ordering = ("date_added",)


class Feed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, blank=True)
    site_url = models.URLField(unique=True, max_length=500, blank=True)
    feed_url = models.URLField(unique=True, max_length=500, help_text="JSON and other feed types coming soon")
    active = models.BooleanField(default=True, db_index=True)
    feed_type = models.SmallIntegerField(choices=FEED_TYPE, default=1)
    feed_display = models.SmallIntegerField(choices=FEED_DISPLAY, default=0)
    #  feed_list = models.ForeignKey(FeedList, related_name='feed_lists', blank=True, null=True, on_delete=models.SET_NULL)
    approval_status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name="feeds", on_delete=models.SET_NULL
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    next_scheduled_update = models.DateTimeField(null=True, blank=True)
    last_story_date = models.DateTimeField(null=True, blank=True)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    num_subscribers = models.IntegerField(default=-1)
    has_feed_exception = models.BooleanField(default=False, db_index=True)
    has_page_exception = models.BooleanField(default=False, db_index=True)
    favicon_color = models.CharField(max_length=6, null=True, blank=True)
    favicon_not_found = models.BooleanField(default=False)
    search_indexed = models.NullBooleanField(default=None, null=True, blank=True)
    pubsub_enabled = models.BooleanField(default=False)
    tags = TaggableManager(through=UUIDTaggedItem, blank=True)
    objects = FeedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/sites/%s/" % (self.slug,)

    def items(self):
        return FeedItem.objects.filter(feed=self)[:6]

    def item_count(self):
        item_counts = FeedItem.objects.filter(feed=self).count()
        return item_counts

    def save(self, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Feed, self).save(**kwargs)
        if settings.SUPERFEEDR_CREDS != None and self.pubsub_enabled == True and self.feed_type == 1:
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
        ordering = ("-title",)


class FeedItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guid = models.CharField(max_length=500, unique=True, db_index=True)
    feed = models.ForeignKey(Feed, blank=True, null=True, on_delete=models.SET_NULL)
    thumbnail_url = models.URLField(max_length=500, blank=True)
    title = models.CharField(max_length=500)
    original_title = models.CharField(max_length=500)
    link = models.URLField(max_length=500)
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager(through=UUIDTaggedItem, blank=True)
    objects = FeedItemManager()

    # def clicks(self):
    #    points = LinkClick.objects.filter(link=self)
    #    return points.count()

    class Meta:
        ordering = ("-date_added",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.link


class FeedListThrough(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    feed = models.ForeignKey(Feed, related_name="group", null=True, on_delete=models.SET_NULL)
    feedlist = models.ForeignKey(FeedList, related_name="group", null=True, on_delete=models.SET_NULL)
    order = models.SmallIntegerField(default=0)

    def __str__(self):
        return "%s is in list %s" % (self.feed, self.feedlist)

    class Meta:
        ordering = ("-order",)


def feed_updated(sender, notification, **kwargs):
    log.debug("Recieved notification on subscription ID %s (%s)", sender.id, sender.topic)
    try:
        feed = Feed.objects.get(feed_url=sender.topic)
    except Feed.DoesNotExist:
        log.error("Subscription ID %s (%s) doesn't have a feed.", sender.id, sender.topic)
        return
    notification = feedparser.parse(notification)

    for entry in notification.entries:
        title = entry.title
        try:
            guid = entry.get("id", entry.link)
        except AttributeError:
            log.error("Feed ID %s has an entry ('%s') without a link or guid. Skipping.", feed.id, title)
        link = getattr(entry, "link", guid)

        content = ""
        if hasattr(entry, "summary"):
            content = entry.summary

        if hasattr(entry, "description"):
            content = entry.description

        # 'content' takes precedence on anything else. 'summary' and
        # 'description' are usually truncated so it's safe to overwrite them
        if hasattr(entry, "content"):
            content = ""
            for item in entry.content:
                content += item.value

        if "published_parsed" in entry and entry.published_parsed is not None:
            date_modified = datetime.datetime(*entry.published_parsed[:6])
        elif "updated_parsed" in entry and entry.updated_parsed is not None:
            date_modified = datetime.datetime(*entry.updated_parsed[:6])
        else:
            date_modified = datetime.datetime.now()

        FeedItem.objects.create_or_update_by_guid(
            guid, feed=feed, title=title, link=link, summary=content, date_updated=date_modified,
        )


push_signals.updated.connect(feed_updated)
