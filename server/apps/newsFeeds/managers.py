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
		return self.active().filter(approval_status=3).filter(is_defunct=False)

	def active(self):
		return super(FeedManager, self).get_queryset().filter(is_defunct=False)
