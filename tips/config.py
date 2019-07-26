import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


def get_sentry_dsn():
    return os.getenv('SENTRY_DSN', None)
