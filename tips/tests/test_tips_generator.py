import datetime
from unittest import TestCase

from tips.api.tip_generator import tips_generator, to_date
from tips.tests.fixtures.fixture import get_fixture

_counter = 0


def get_tip(priority=50):
    global _counter
    counter = _counter
    _counter += 1
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


class HelperFunctionsTests(TestCase):
    def test_to_date(self):
        # valid
        result = to_date('1950-01-01T00:00:00Z')
        self.assertEqual(result, datetime.datetime(year=1950, month=1, day=1, tzinfo=datetime.timezone.utc))

        # valid
        result = to_date('1950-01-01')
        self.assertEqual(result, datetime.datetime(year=1950, month=1, day=1))

        # invalid
        with self.assertRaises(ValueError):
            result = to_date('not a date')
            self.assertEqual(result, datetime.datetime(year=1950, month=1, day=1, tzinfo=datetime.timezone.utc))


class TipsGeneratorTest(TestCase):
    def setUp(self) -> None:
        pass

    def get_client_data(self):
        return get_fixture()

    def test_generator(self):
        tip0 = get_tip(10)
        tip1 = get_tip(20)
        tip2 = get_tip(30)
        tip3 = get_tip(40)
        tip4 = get_tip(50)

        tip4['conditional'] = "False"

        # add them out of order to test the ordering
        tips_pool = [tip1, tip0, tip2, tip3]
        result = tips_generator(self.get_client_data(), tips_pool)
        tips = result['items']

        self.assertEqual(len(tips), 4)

        # check order
        self.assertEqual(tips[3]['id'], tip0['id'])
        self.assertEqual(tips[2]['id'], tip1['id'])
        self.assertEqual(tips[1]['id'], tip2['id'])
        self.assertEqual(tips[0]['id'], tip3['id'])


class ConditionalTest(TestCase):
    def get_client_data(self, optin=False):
        return get_fixture(optin)

    def test_active(self):
        """ Add one active and one inactive tip. """

        tip1_mock = get_tip()
        tip1_mock['active'] = False
        tip2_mock = get_tip()

        tips_pool = [tip1_mock, tip2_mock]

        result = tips_generator(self.get_client_data(), tips_pool)
        tips = result['items']
        self.assertEqual(len(tips), 1)

        # Test if the correct ones are accepted
        ids = [tip['id'] for tip in tips]
        self.assertEqual(ids, [tip2_mock['id']])

    def test_conditional(self):
        """ Test one passing conditional, one failing and one without (the default) """
        tip1_mock = get_tip()
        tip1_mock['conditional'] = "False"
        tip2_mock = get_tip()
        tip2_mock['conditional'] = "True"
        tip3_mock = get_tip()

        tips_pool = [tip1_mock, tip2_mock, tip3_mock]
        result = tips_generator(self.get_client_data(), tips_pool)
        tips = result['items']
        self.assertEqual(len(tips), 2)

        # Test if the correct ones are accepted
        ids = [tip['id'] for tip in tips]
        self.assertEqual(ids, [tip2_mock['id'], tip3_mock['id']])

    def test_conditional_exception(self):
        """ Test that invalid conditional is (silently) ignored. Probably not the best idea... """
        tip1_mock = get_tip()
        tip1_mock['conditional'] = "syntax error"
        tip2_mock = get_tip()

        tips_pool = [tip1_mock, tip2_mock]
        result = tips_generator(self.get_client_data(), tips_pool)
        tips = result['items']

        # make sure the other is in there
        self.assertEqual(len(tips), 1)
        self.assertEqual(tips[0]['id'], tip2_mock['id'])

    def test_conditional_invalid(self):
        """ Test that it errors on completely wrong conditional. """
        tip1_mock = get_tip()
        tip1_mock['conditional'] = True
        tip2_mock = get_tip()

        tips_pool = [tip1_mock, tip2_mock]
        with self.assertRaises(TypeError):
            tips_generator(self.get_client_data(), tips_pool)

    def test_data_based_tip(self):
        """
        Test whether a tip works correctly when based on user data.
        """
        tip1_mock = get_tip()
        tip1_mock['conditional'] = "data['erfpacht'] == True"
        tip2_mock = get_tip()
        tips_pool = [tip1_mock, tip2_mock]

        client_data = self.get_client_data(optin=True)

        result = tips_generator(client_data, tips_pool)
        tips = result['items']

        # make sure the other is in there
        self.assertEqual(len(tips), 2)

    def test_data_based_tip_path(self):
        tip1_mock = get_tip()
        tip1_mock['conditional'] = "value_of(data, 'erfpacht') == True"
        tip2_mock = get_tip()
        # 18 or older
        tip2_mock['conditional'] = "before(value_of(data, 'brp.persoon.geboortedatum'), years=18)"
        tips_pool = [tip1_mock, tip2_mock]

        client_data = self.get_client_data(optin=True)

        result = tips_generator(client_data, tips_pool)
        tips = result['items']

        # make sure the other is in there
        self.assertEqual(len(tips), 2)
        self.assertEqual(tips[0]['id'], 0)
        self.assertEqual(tips[1]['id'], 1)
