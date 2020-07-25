from datetime import datetime, timedelta
import requests
import string
import random
import logging

logger = logging.getLogger("default")


def human_readable_milliseconds(milliseconds):
    milliseconds = int(milliseconds)
    seconds = int((milliseconds / 1000) % 60)
    minutes = int((milliseconds / (1000 * 60)) % 60)
    hours = int((milliseconds / (1000 * 60 * 60)) % 24)
    result = ""
    if hours:
        result += "{0} hours ".format(hours)
    if minutes:
        result += "{0} minutes ".format(minutes)
    if seconds:
        result += "{0} seconds".format(seconds)
    return result


def human_readable_seconds(orig_seconds):
    seconds = int(orig_seconds % 60)
    minutes = int((orig_seconds / 60) % 60)
    hours = int((orig_seconds / (60 * 60)) % 24)
    result = ""
    if hours:
        result += "{0} hours <br />".format(hours)
    if minutes:
        result += "{0} minutes ".format(minutes)
    # if seconds:
    #    result += "{0} seconds".format(seconds)
    return result
