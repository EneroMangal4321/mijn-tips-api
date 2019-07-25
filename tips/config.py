import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

SENTRY_DSN = os.getenv('SENTRY_DSN', None)
