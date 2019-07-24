import sentry_sdk
from flask import Flask, request
from sentry_sdk.integrations.flask import FlaskIntegration

from tips.api.tip_generator import tips_generator
from tips.config import SENTRY_DSN

app = Flask(__name__)


if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        with_locals=True
    )


@app.route('/gettips', methods=['POST'])
def hello_world():
    tips_data = tips_generator(request.get_json())
    return tips_data


@app.route('/status/health')
def health_check():
    return 'OK'


if __name__ == '__main__':
    app.run()
