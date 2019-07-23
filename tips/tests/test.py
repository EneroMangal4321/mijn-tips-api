from pprint import pprint

from flask_testing import TestCase

from tips.server import app
from tips.tests.fixtures.fixture import get_fixture


class ApiTests(TestCase):
    def create_app(self):
        return app

    def test_tips(self):
        pprint(get_fixture())


