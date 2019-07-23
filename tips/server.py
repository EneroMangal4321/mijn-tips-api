import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

from tips.config import SENTRY_DSN

app = Flask(__name__)


if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        with_locals=True
    )


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
