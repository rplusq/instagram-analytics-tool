import random
from time import sleep
from datetime import datetime
import json
from igramscraper.instagram import Instagram
from functools import reduce

def media_filter(media, start_year, start_month, end_year, end_month):
    created_at_datetime = datetime.fromtimestamp(media.created_time)
    media_year = created_at_datetime.year
    media_month = created_at_datetime.month
    # If the year is lesser than the starting one
    if media_year < start_year:
        return False
    # If the year is greater than the starting one
    elif media_year > end_year:
        return False
    # If the year is between the expected years
    else:
        # False if equal to start year but lesser than start month
        if media_year == start_year and media_month < start_month:
            return False
        # False if equal to end year but greater end start month
        if media_year == end_year and media_month > end_month:
            return False
        # Edge cases checked, return True
        else:
            return True
    return False

def get_info_from_api(username, media_count,start_year, start_month, end_year=datetime.now().year, end_month=datetime.now().month):
    instagram = Instagram()
    results = dict()
    results["account"] = instagram.get_account(username).__dict__
    # We sleep between calls
    sleep(random.uniform(15,30))
    # We filter the media that doesn't meet the requirements
    unfiltered_medias = instagram.get_medias(username, media_count)
    filtered_media = list(filter(lambda media: media_filter(media,start_year,start_month,end_year,end_month), unfiltered_medias))
    results["medias"] = (list(map(lambda media: media.__dict__,filtered_media)))
    return results

def date_validator(media_month, media_year, start_year, start_month, end_year, end_month):
    # If the year is lesser than the starting one
    if media_year < start_year:
        return False
    # If the year is greater than the starting one
    elif media_year > end_year:
        return False
    # If the year is between the expected years
    else:
        # False if equal to start year but lesser than start month
        if media_year == start_year and media_month < start_month:
            return False
        # False if equal to end year but greater end start month
        if media_year == end_year and media_month > end_month:
            return False
        # Edge cases checked, return True
        else:
            return True
    return False