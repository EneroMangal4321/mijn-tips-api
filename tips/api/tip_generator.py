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

FRONT_END_TIP_KEYS = ['datePublished', 'description', 'id', 'link', 'title', 'priority']


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
        eval_locals = {}
        print("optin", userdata['optin'])
        if userdata['optin']:
            eval_locals['data'] = userdata['data']

        # from pprint import pprint
        # print("--------------")
        # print(conditional)
        # pprint(eval_locals)

        if eval(conditional, EVAL_GLOBALS, eval_locals):
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
