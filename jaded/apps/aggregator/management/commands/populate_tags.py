import json
import os
from time import strftime
from hashlib import md5
import datetime
from optparse import make_option
from bs4 import BeautifulSoup
import threading
import queue

from django.core.management.base import BaseCommand

from aggregator.models import FeedList, Feed, FeedItem
from aggregator.utils import generate_summary


class Command(BaseCommand):
    help = "Add tags based on text summary."

    def handle(self, *args, **kwargs):
        try:
            self.add_tags(verbose=False, num_threads=1)
        finally:
            print("Cleaning up.")

    def add_tags(self, verbose=False, num_threads=4):
        queryset = FeedItem.objects.all()[:5]
        print("Processing results...")
        for obj in queryset:
            description = obj.summary
            summary = BeautifulSoup(obj.summary, "html.parser")
            print("generating summary...")
            # print(summary.get_text())
            summary_text = generate_summary(summary.get_text(), 4)
        return summary_text
