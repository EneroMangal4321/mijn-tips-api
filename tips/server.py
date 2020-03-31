import connexion
import sentry_sdk
import os
import json

from tips.config import PROJECT_PATH
from flask import request, send_from_directory
from sentry_sdk.integrations.flask import FlaskIntegration

from tips.api.tip_generator import tips_generator
from tips.config import get_sentry_dsn, get_photo_path

PERSOONLIJK_INKOMENS_TIPS_FILE = os.path.join(PROJECT_PATH, 'api', 'persoonlijk_inkomens_tips.json')


app = connexion.FlaskApp(__name__, specification_dir='openapi/')

if get_sentry_dsn():  # pragma: no cover
    sentry_sdk.init(
        dsn=get_sentry_dsn(),
        integrations=[FlaskIntegration()],
        with_locals=False
    )


# Route is defined in swagger/tips.yaml
def get_tips():
    # This is a POST because the user data gets sent in the body.
    # This data is too large and inappropriate for a GET, also because of privacy reasons
    tips_data = tips_generator(request.get_json())
    return tips_data

def get_income_tips():
    # This is a POST because the user data gets sent in the body.
    # This data is too large and inappropriate for a GET, also because of privacy reasons
    with open(PERSOONLIJK_INKOMENS_TIPS_FILE) as fp:
        persoonlijk_inkomens_tips = json.load(fp)
    tips_data = tips_generator(request.get_json(),persoonlijk_inkomens_tips)
    return tips_data


@app.route('/tips/static/tip_images/<path:filename>')
def download_file(filename):
    return send_from_directory(get_photo_path(), filename, as_attachment=True)


@app.route('/status/health')
def health_check():
    return 'OK'


app.add_api('tips.yaml')

# set the WSGI application callable to allow using uWSGI:
application = app.app
if __name__ == '__main__':  # pragma: no cover
    app.run()
