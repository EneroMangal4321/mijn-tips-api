import datetime
import json
import os
from typing import Union

import dateutil.parser
import pytz

from tips.config import PROJECT_PATH
"""

    {
        "priority": 0,
        "datePublished": "2019-07-24",
        "title": "",
        "subtitle": "",
        "description": "",
        "link": {
            "title": "",
            "to": ""
        }
    },

"""

TIPS_POOL_FILE = os.path.join(PROJECT_PATH, 'api', 'tips_pool.json')

FRONT_END_TIP_KEYS = ['datePublished', 'description', 'id', 'link', 'title', 'priority']


tips_pool = []


def value_of(data: dict, path: str, default=None):
    """
    Try to get the value of path '.' with as separator. When not possible, return the default.
    :param data: data in which to search for
    :param path: . separated path to the nested data
    :param default: value which is returned when path is not found
    :return: The value of path when found, otherwise default.

    TODO: how to deal with lists?
    """
    path_sep = path.split('.')
    value = data
    for part in path_sep:
        try:
            value = value[part]
        except KeyError:
            return default
    return value


def to_date(value: str):
    """ Converts a string containing an iso8601 date to a datetime object. """
    # 1950-01-01T00:00:00Z
    date = dateutil.parser.isoparse(value)

    return date


def is_18(value: Union[datetime.date, datetime.datetime]):
    return before_or_on(value, years=18)


# TODO: better name
def before_or_on(value: datetime.datetime, **kwargs):
    """
    Check if the value is before or on the specified timedelta values.
    The keyword arguments are fed into a dateutils relative timedelta
    https://dateutil.readthedocs.io/en/stable/relativedelta.html

    """
    delta = dateutil.relativedelta.relativedelta(**kwargs)

    if type(value) == str:
        value = to_date(value)

    if type(value) == datetime.datetime:
        now = datetime.datetime.now(datetime.timezone.utc)

        # Set utz for dates which have no timezone
        if value.tzinfo is None:
            value = pytz.UTC.localize(value)

        result = value <= now - delta
        return result
    elif type(value) == datetime.date:
        # Date has no timezone
        today = datetime.date.today()
        result = value <= today - delta
        return result


EVAL_GLOBALS = {
    "datetime": datetime.datetime,
    "timedelta": dateutil.relativedelta.relativedelta,
    "before_or_on": before_or_on,
    "value_of": value_of,
    "to_date": to_date,
    "is_18": is_18,
    "len": len,
}


def refresh_tips_pool():
    global tips_pool
    with open(TIPS_POOL_FILE) as fh:
        tips_pool = json.load(fh)


refresh_tips_pool()


def tip_filterer(tip, userdata):
    # if a tip has a conditional field, it must be true. If it does not. it's always included
    if not tip['active']:
        return False
    conditional = tip.get("conditional", None)
    if conditional is None:
        return tip
    try:
        eval_locals = {}
        if userdata['optin']:
            eval_locals['data'] = userdata['data']
        # print("\n------\noptin", userdata['optin'])
        # print("trying ", conditional)

        if eval(conditional, EVAL_GLOBALS, eval_locals):
            # print("True")
            return tip
        else:
            return False
    except TypeError:  # Input must be a string. If its anything else, the tip conditional is malformed
        raise
    except Exception as e:
        print("!! Conditional exception: ", e)
        return False


def clean_tip(tip):
    """ Only select the relevant frontend fields. """
    return {k: v for (k, v) in tip.items() if k in FRONT_END_TIP_KEYS}


def tips_generator(user_data, tips=None):
    """ Generate tips. """
    if tips is None:
        tips = tips_pool
    tips = [tip for tip in tips if tip_filterer(tip, user_data)]
    tips = [clean_tip(tip) for tip in tips]

    tips.sort(key=lambda t: t['priority'], reverse=True)

    return {
        "items": tips,
        "total": len(tips),
    }
