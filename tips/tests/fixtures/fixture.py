import json
import os

_FIXTURE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


# these fixtures are copied from the frontend
BRP = os.path.join(_FIXTURE_PATH, "brp.json")
FOCUS = os.path.join(_FIXTURE_PATH, "focus.json")
WMO = os.path.join(_FIXTURE_PATH, "brp.json")


def get_fixture():
    with open(BRP) as brp_file:
        brp = json.load(brp_file)

    with open(FOCUS) as focus_file:
        focus = json.load(focus_file)

    with open(WMO) as wmo_file:
        wmo = json.load(wmo_file)

    return {
        "optin": False,
        "data": {
            "brp": brp,
            "focus": focus,
            "wmo": wmo,
        }
    }
