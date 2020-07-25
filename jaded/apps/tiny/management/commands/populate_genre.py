import json
import os
import urllib
from time import strftime
from hashlib import md5
import datetime
from optparse import make_option

from django.core.management.base import BaseCommand
from tiny.models import Genre

API_KEY = "api_key=acc17f392b86ce1d3ce742f0200f97a267512a34"
RELEASE_URL = "https://www.giantbomb.com/api/genres/?"
FIELDS = "format=json"


class Command(BaseCommand):
    help = "Populates the genres model from json feed"

    def add_arguments(self, parser):
        parser.add_argument(
            "-o", "--offset", metavar="NUM", type=int, default=0, help="offsets list by X. Defaults to 0"
        )

    def handle(self, *args, **kwargs):

        # Takes a list of results, and updates the db with results.
        def process_results(results):
            for result in results:
                # Create genre object
                genre_name = result["name"]
                genre_id = result["id"]

                # GUID Generation
                guid_base = "%s-%s" % (genre_id, genre_name)
                guid_encoded = guid_base.encode("ascii", "ignore")
                guid = md5(guid_encoded).hexdigest()[:12]

                Genre.objects.create_or_update_by_guid(
                    guid, id=genre_id, name=genre_name,
                )

        # Grab 100 entries at a time (the limit)
        # Call the api to get the first 100 entries:
        # To do pagination, add &offset=<offset> to the query
        try:
            url = RELEASE_URL + API_KEY + "&" + FIELDS
            offset = kwargs["offset"]
            response = urllib.request.urlopen("{0}&offset={1}".format(url, offset))
            json_data = json.load(response)
            # Find out how many total entries there are:
            total_entries = json_data["number_of_total_results"]
            # Process the first results
            print("Processing first 100 results...")
            process_results(json_data["results"])

            # Loop every 100 up to how many total entries there are.
            offset = int(offset) + 100
            while not offset > total_entries:
                print("Processing next 100 results, offset by {0} results...".format(offset))
                response = urllib.request.urlopen("{0}&offset={1}".format(url, offset))
                json_data = json.load(response)
                process_results(json_data["results"])
                offset += 100
        finally:
            print("Writing genres complete!")
