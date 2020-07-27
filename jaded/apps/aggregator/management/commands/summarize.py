import json
import os
from time import strftime
from hashlib import md5
import datetime
from optparse import make_option
from bs4 import BeautifulSoup
import threading
import queue
import logging
import socket
import datetime
from bpe_summarizer import bpe_summarize

from django.core.management.base import BaseCommand

from aggregator.models import FeedList, Feed, FeedItem
from aggregator.utils import generate_summary, read_article


class Command(BaseCommand):
    help = "Creates a summary based on description field."
    LOCKFILE = "/tmp/sumarize_feed_items.lock"

    def add_arguments(self, parser):
        parser.add_argument(
            "-t", "--threads", metavar="NUM", type=int, default=4, help="Number of updater threads (default: 4)."
        )

    def handle(self, *args, **kwargs):
        log = self.setup_logging()
        log.debug("Starting run.")
        total_threads = kwargs["threads"]

        try:
            lockfile = os.open(self.LOCKFILE, os.O_CREAT | os.O_EXCL)
        except OSError:
            print >>sys.stderr, "Lockfile exists (%s). Aborting." % self.LOCKFILE
            sys.exit(1)
        try:
            verbose = int(kwargs["verbosity"]) > 0
        except (KeyError, TypeError, ValueError):
            verbose = True
        try:
            self.description_to_summary(verbose=verbose, num_threads=kwargs["threads"])
        except:
            log.exception("Uncaught exception updating feeditems.")
        finally:
            log.debug("Cleaning up.")
            os.close(lockfile)
            os.unlink(self.LOCKFILE)
        log.debug("Ending run.")

    def description_to_summary(self, verbose=True, num_threads=4):
        feeditem_queue = queue.Queue()
        for feeditem in FeedItem.objects.all():
            feeditem_queue.put(feeditem)
        threadpool = []
        for i in range(num_threads):
            threadpool.append(SummaryWorker(q=feeditem_queue, verbose=verbose))

        [t.start() for t in threadpool]
        [t.join() for t in threadpool]

    def setup_logging(self):
        log = logging.getLogger("django_website.sumarize_feed_items")
        log.setLevel(logging.DEBUG)
        handler = logging.FileHandler("sumarize_feed_items.log")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] (%(thread)d) %(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)
        return log


class SummaryWorker(threading.Thread):
    def __init__(self, q, verbose, **kwargs):
        super(SummaryWorker, self).__init__(**kwargs)
        self.daemon = True
        self.verbose = verbose
        self.q = q
        self.log = logging.getLogger("jaded.summarize")

    def run(self):
        while 1:
            try:
                feeditem = self.q.get_nowait()
            except queue.Empty:
                return
            self.summarize_feeditem(feeditem)
            self.q.task_done()

    def summarize_feeditem(self, feeditem):
        self.log.debug("Starting update: %s." % feeditem)

        if self.verbose:
            print(feeditem)

        try:
            socket.setdefaulttimeout(15)
            description = feeditem.summary
            guid = feeditem.guid
            date_modified = datetime.datetime.now()
            if description:
                summary = BeautifulSoup(description, "html.parser")
                print("generating summary...")
                if len(summary.get_text()) >= 500:
                    # summary_text = generate_summary(summary.get_text(), 4)
                    summary_text = bpe_summarize(summary.get_text(), percentile=99)
                else:
                    summary_text = summary.get_text()
                # print(summary_text)
                FeedItem.objects.create_or_update_by_guid(guid, description=summary_text, date_updated=date_modified)
            else:
                print("skipping, no description found.")
        except Exception:
            self.log.exception("Error updating %s." % feeditem)
            return

        self.log.debug("Done with %s." % feeditem)
