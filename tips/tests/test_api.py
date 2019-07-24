import json
from pprint import pprint

from flask_testing import TestCase

from tips.server import app
from tips.tests.fixtures.fixture import get_fixture


class ApiTests(TestCase):
    def create_app(self):
        return app

    def get_client_data(self):
        return get_fixture()

    def test_status(self):
        response = self.client.get('/status/health')
        self.assert200(response)
        self.assertEqual(response.data, b"OK")

    def test_tips(self):
        response = self.client.post('/gettips', json=self.get_client_data())
        pprint(json.loads(response.data))
        print(response.mimetype)
