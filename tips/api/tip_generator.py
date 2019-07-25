import datetime
import json
import os

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


tips_pool = []

EVAL_GLOBALS = {
    "datetime": datetime.datetime
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
        print("trying ", conditional)
        if eval(conditional, EVAL_GLOBALS, {}):
            return tip
        else:
            return False
    except TypeError:  # Input must be a string. If its anything else, the tip conditional is malformed
        raise
    except Exception as e:
        print("!! Error", e)
        return False


def tips_generator(user_data, tips=None):
    """ Generate tips. """
    if tips is None:
        tips = tips_pool
    tips = [tip for tip in tips if tip_filterer(tip, user_data)]

    tips.sort(key=lambda t: t['priority'], reverse=True)

    return {
        "tips": tips
    }
