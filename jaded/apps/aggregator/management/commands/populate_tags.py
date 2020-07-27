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

from django.core.management.base import BaseCommand

from aggregator.models import FeedList, Feed, FeedItem
from aggregator.utils import generate_summary
from tiny.models import Genre


class Command(BaseCommand):
    help = "Generates tags based on titles"
    LOCKFILE = "/tmp/tag_feed_items.lock"

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
            self.filter_tags(verbose=verbose, num_threads=kwargs["threads"])
        except:
            log.exception("Uncaught exception updating feeditems.")
        finally:
            log.debug("Cleaning up.")
            os.close(lockfile)
            os.unlink(self.LOCKFILE)
        log.debug("Ending run.")

    def filter_tags(self, verbose=True, num_threads=4):
        feeditem_queue = queue.Queue()
        for feeditem in FeedItem.objects.all()[:3]:
            feeditem_queue.put(feeditem)
        threadpool = []
        for i in range(num_threads):
            threadpool.append(TagsWorker(q=feeditem_queue, verbose=verbose))

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


class TagsWorker(threading.Thread):
    def __init__(self, q, verbose, **kwargs):
        super(TagsWorker, self).__init__(**kwargs)
        self.daemon = True
        self.verbose = verbose
        self.q = q
        self.log = logging.getLogger("jaded.populate_tags")

    def run(self):
        while 1:
            try:
                feeditem = self.q.get_nowait()
            except queue.Empty:
                return
            self.check_for_tags(feeditem)
            self.q.task_done()

    def check_for_tags(self, feeditem):
        self.log.debug("Starting update: %s." % feeditem)

        tags_list = ["Halo"]
        genres = Genre.objects.all()
        for genre in genres:
            tags_list.append(genre.name)

        if self.verbose:
            print(feeditem)

        try:
            socket.setdefaulttimeout(15)
            guid = feeditem.guid
            title = feeditem.title
            title_list = title.split()
            tokens_sw = list(set(title_list) & set(tags_list))

            # print(title_list)
            # print(tags_list)

            # date_modified = datetime.datetime.now()
            if tokens_sw:
                print("generating tag list...")
                print(tokens_sw)
                # FeedItem.objects.create_or_update_by_guid(guid, description=summary_text, date_updated=date_modified)
            else:
                print("skipping, no tags found.")
        except Exception:
            self.log.exception("Error updating %s." % feeditem)
            return

        self.log.debug("Done with %s." % feeditem)
