import logging
import datetime
import feedparser
from time import strftime
from hashlib import md5

from django.db import models
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)


class NewsItemManager(models.Manager):
    def public(self):
        return super(NewsItemManager, self).get_queryset().filter(is_hidden=False)
