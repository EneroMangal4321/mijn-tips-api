from pprint import pprint
from unittest import TestCase

from tips.api.tip_generator import tips_generator
from tips.tests.fixtures.fixture import get_fixture


class TipsGeneratorTest(TestCase):
    def setUp(self) -> None:
        pass

    def get_client_data(self):
        return get_fixture()

    def test_generator(self):
        tips = tips_generator(self.get_client_data())
        pprint(tips)

    def test_refreshing_tips_pool(self):
        pass


class ConditionalTest(TestCase):
    _counter = 0

    def get_tip(self, priority=50):
        counter = self._counter
        self._counter += 1
        return {
            'id': counter,
            'active': True,
            'priority': priority,
            'datePublished': '2019-07-24',
            'description': 'Tip description %i' % counter,
            'link': {
                'title': 'Tip link title %i' % counter,
                'to': 'https://amsterdam.nl/'
            },
            'title': 'Tip title %i' % counter
        }

    def get_client_data(self):
        return get_fixture()

    def test_active(self):
        """ Add one active and one inactive tip. """

        tip1_mock = self.get_tip()
        tip1_mock['active'] = False
        tip2_mock = self.get_tip()

        tips_pool = [tip1_mock, tip2_mock]

        result = tips_generator(self.get_client_data(), tips_pool)
        tips = result['tips']
        self.assertEqual(len(tips), 1)

        # Test if the correct ones are accepted
        ids = [tip['id'] for tip in tips]
        self.assertEqual(ids, [tip2_mock['id']])

    def test_conditional(self):
        """ Test one passing conditional, one failing and one without (the default) """
        tip1_mock = self.get_tip()
        tip1_mock['conditional'] = "False"
        tip2_mock = self.get_tip()
        tip2_mock['conditional'] = "True"
        tip3_mock = self.get_tip()

        tips_pool = [tip1_mock, tip2_mock, tip3_mock]
        result = tips_generator(self.get_client_data(), tips_pool)
        tips = result['tips']
        self.assertEqual(len(tips), 2)

        # Test if the correct ones are accepted
        ids = [tip['id'] for tip in tips]
        self.assertEqual(ids, [tip2_mock['id'], tip3_mock['id']])

    def test_conditional_exception(self):
        """ Test that invalid conditional is ignored. Probably not the best idea... """
        tip1_mock = self.get_tip()
        tip1_mock['conditional'] = "syntax error"
        tip2_mock = self.get_tip()

        tips_pool = [tip1_mock, tip2_mock]
        result = tips_generator(self.get_client_data(), tips_pool)
        tips = result['tips']

        # make sure the other is in there
        self.assertEqual(len(tips), 1)
        self.assertEqual(tips[0]['id'], tip2_mock['id'])

    def test_conditional_invalid(self):
        """ Test that it errors on completely wrong conditional. """
        tip1_mock = self.get_tip()
        tip1_mock['conditional'] = True
        tip2_mock = self.get_tip()

        tips_pool = [tip1_mock, tip2_mock]
        with self.assertRaises(TypeError):
            tips_generator(self.get_client_data(), tips_pool)


