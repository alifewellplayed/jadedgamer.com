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

from django.core.management.base import BaseCommand

from aggregator.models import FeedList, Feed, FeedItem
from aggregator.utils import generate_summary


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

    def description_to_summary(self, verbose=False, num_threads=4):
        feeditem_queue = queue.Queue()
        for feeditem in FeedItem.objects.all()[:5]:
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
            summary = BeautifulSoup(feeditem.summary, "html.parser")
            print("generating summary...")
            summary_text = generate_summary(summary.get_text(), 2)
            print(summary_text)
        except Exception:
            self.log.exception("Error updating %s." % feeditem)
            return

        self.log.debug("Done with %s." % feeditem)
