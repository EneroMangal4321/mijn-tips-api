import sentry_sdk
from flask import Flask, request, send_from_directory
from sentry_sdk.integrations.flask import FlaskIntegration

from tips.api.tip_generator import tips_generator
from tips.config import get_sentry_dsn, get_photo_path

app = Flask(__name__)


if get_sentry_dsn():  # pragma: no cover
    sentry_sdk.init(
        dsn=get_sentry_dsn(),
        integrations=[FlaskIntegration()],
        with_locals=False
    )


@app.route('/tips/gettips', methods=['POST'])
def hello_world():
    tips_data = tips_generator(request.get_json())
    return tips_data


@app.route('/tips/static/tip_images/<path:filename>')
def download_file(filename):
    return send_from_directory(get_photo_path(), filename, as_attachment=True)


@app.route('/status/health')
def health_check():
    return 'OK'


if __name__ == '__main__':  # pragma: no cover
    app.run()
