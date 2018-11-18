import logging
import datetime
import feedparser
from time import strftime
from hashlib import md5

from django.db import models
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)

class FeedManager(models.Manager):
	def approved(self):
		return self.active().filter(approval_status=3)

	def active(self):
		return super(FeedManager, self).get_queryset().filter(active=True)


class FeedItemManager(models.Manager):
    def create_or_update_by_guid(self, guid, **kwargs):
        """
        Look up a FeedItem by GUID, updating it if it exists, and creating
        it if it doesn't.
        We don't limit it by feed because an item could be in another feed if
        some feeds are themselves aggregators. That's also why we don't update
        the feed field if the feed item already exists.
        Returns (item, created) like get_or_create().
        """
        try:
            item = self.get(guid=guid)
        except self.model.DoesNotExist:
            # Create a new item
            log.debug('Creating entry: %s', guid)
            kwargs['guid'] = guid
            item = self.create(**kwargs)
        else:
            log.debug('Updating entry: %s', guid)

            # Update an existing one.
            kwargs.pop('feed', None)

            # Don't update the date since most feeds get this wrong.
            kwargs.pop('date_modified')

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item
