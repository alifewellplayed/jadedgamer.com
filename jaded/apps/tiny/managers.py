import logging
import datetime
import feedparser
from time import strftime
from hashlib import md5

from django.db import models
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)


class NameManager(models.Manager):
    def get_by_natural_key(self, some_name):
        return self.get(name=some_name)


class UpdateManager(models.Manager):
    def create_or_update_by_guid(self, guid, **kwargs):
        try:
            item = self.get(guid=guid)

        except self.model.DoesNotExist:
            # Create a new item
            log.debug("Creating entry: %s", guid)
            kwargs["guid"] = guid
            item = self.create(**kwargs)

        else:
            log.debug("Updating entry: %s", guid)

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item

    def create_or_update_by_id(self, id, **kwargs):
        try:
            item = self.get(id=id)

        except self.model.DoesNotExist:
            # Create a new item
            log.debug("Creating entry: %s", id)
            kwargs["id"] = id
            item = self.create(**kwargs)

        else:
            log.debug("Updating entry: %s", id)

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item


class CompanyManager(models.Manager):
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
            log.debug("Creating entry: %s", guid)
            kwargs["guid"] = guid
            item = self.create(**kwargs)

        else:
            log.debug("Updating entry: %s", guid)

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item


class GenreManager(models.Manager):
    def create_or_update_by_guid(self, guid, **kwargs):
        """
        Look up a Genre by GUID, updating it if it exists, and creating
        it if it doesn't.

        Returns (item, created) like get_or_create().
        """
        try:
            item = self.get(guid=guid)

        except self.model.DoesNotExist:
            # Create a new item
            log.debug("Creating entry: %s", guid)
            kwargs["guid"] = guid
            item = self.create(**kwargs)

        else:
            log.debug("Updating entry: %s", guid)

            # Don't update the date since most feeds get this wrong.
            kwargs.pop("date_added")

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item


class ThemeManager(models.Manager):
    def create_or_update_by_guid(self, guid, **kwargs):
        try:
            item = self.get(guid=guid)

        except self.model.DoesNotExist:
            # Create a new item
            log.debug("Creating entry: %s", guid)
            kwargs["guid"] = guid
            item = self.create(**kwargs)

        else:
            log.debug("Updating entry: %s", guid)

            # Don't update the date added
            kwargs.pop("date_added")

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item


class PlatformManager(models.Manager):
    def create_or_update_by_guid(self, guid, **kwargs):
        try:
            item = self.get(guid=guid)

        except self.model.DoesNotExist:
            # Create a new item
            log.debug("Creating entry: %s", guid)
            kwargs["guid"] = guid
            item = self.create(**kwargs)

        else:
            log.debug("Updating entry: %s", guid)

            # Don't update the date added
            kwargs.pop("date_added")

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item


class RatingManager(models.Manager):
    def create_or_update_by_guid(self, guid, **kwargs):
        try:
            item = self.get(guid=guid)

        except self.model.DoesNotExist:
            # Create a new item
            log.debug("Creating entry: %s", guid)
            kwargs["guid"] = guid
            item = self.create(**kwargs)

        else:
            log.debug("Updating entry: %s", guid)

            # Don't update the date added
            kwargs.pop("date_added")

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item


class RegionManager(models.Manager):
    def create_or_update_by_guid(self, guid, **kwargs):
        try:
            item = self.get(guid=guid)

        except self.model.DoesNotExist:
            # Create a new item
            log.debug("Creating entry: %s", guid)
            kwargs["guid"] = guid
            item = self.create(**kwargs)

        else:
            log.debug("Updating entry: %s", guid)

            # Don't update the date added
            kwargs.pop("date_added")

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item


class FranchiseManager(models.Manager):
    def create_or_update_by_guid(self, guid, **kwargs):
        try:
            item = self.get(guid=guid)

        except self.model.DoesNotExist:
            # Create a new item
            log.debug("Creating entry: %s", guid)
            kwargs["guid"] = guid
            item = self.create(**kwargs)

        else:
            log.debug("Updating entry: %s", guid)

            # Don't update the date added
            kwargs.pop("date_added")

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item


class GameManager(models.Manager):
    def create_or_update_by_guid(self, guid, **kwargs):
        try:
            item = self.get(guid=guid)

        except self.model.DoesNotExist:
            # Create a new item
            log.debug("Creating entry: %s", guid)
            kwargs["guid"] = guid
            item = self.create(**kwargs)

        else:
            log.debug("Updating entry: %s", guid)

            # Don't update the date added
            kwargs.pop("date_added")

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item


class ReleaseManager(models.Manager):
    def create_or_update_by_guid(self, guid, **kwargs):
        try:
            item = self.get(guid=guid)

        except self.model.DoesNotExist:
            # Create a new item
            log.debug("Creating entry: %s", guid)
            kwargs["guid"] = guid
            item = self.create(**kwargs)

        else:
            log.debug("Updating entry: %s", guid)

            # Don't update the date added
            kwargs.pop("date_added")

            for k, v in kwargs.items():
                setattr(item, k, v)
            item.save()

        return item
