import json
import os
from time import strftime
from hashlib import md5
import datetime
from optparse import make_option
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand

from aggregator.models import FeedList, Feed, FeedItem
from aggregator.utils import generate_summary

class Command(BaseCommand):
  help = 'Creates a summary based on description field.'

  def handle(self, *args, **kwargs):
    try:
      self.description_to_summary(verbose=False, num_threads=1)
    finally:
      print('Cleaning up.')

  def description_to_summary(self, verbose=False, num_threads=4):
    queryset = FeedItem.objects.all()[:5]
    print("Processing results...")
    for obj in queryset:
      description = obj.summary
      summary = BeautifulSoup(obj.summary, , 'html.parser')
      print('generating summary...')
      #print(summary.get_text())
      summary_text = generate_summary(summary.get_text(), 2)
    return summary_text

