import os
from pprint import pprint

from flask_testing import TestCase

from tips.api.tip_generator import tips_pool
from tips.config import PROJECT_PATH
from tips.server import application
from tips.tests.fixtures.fixture import get_fixture

class ApiTests(TestCase):
    def create_app(self):
        app = application
        app.config['TESTING'] = True
        return app

    def _get_client_data(self):
        return get_fixture(optin=True)

    def test_tips(self):
        response = self.client.post('/tips/getincometips', json=self._get_client_data())

        data = response.get_json()
        tips = data['items']
        pprint(tips)
        self.assertEqual(len(tips), len(tips))
