from unittest import TestCase

import objectpath
import json
from pprint import pprint

from tips.generator.rule_engine import apply_rules

from tips.tests.fixtures.fixture import get_fixture

with open("C:/xampp/htdocs/Stage_Amsterdam/mijn-tips-api/tips/api/compound_rules.json") as compound_rules_file:
    compound_rules = json.load(compound_rules_file)

# with open("C:/xampp/htdocs/Stage_Amsterdam/mijn-tips-api/tips/api/persoonlijk_inkomens_tips.json") as rules_file:
#     rules = json.load(rules_file)


class RuleEngineTest(TestCase):
    def setUp(self) -> None:
        _test_data = {
            'a': [ 
                1, 2, 3
            ],
            'b': [
                {'x': True, 'y': True},
                {'x': True, 'y': False},
                {'x': False, 'y': True}
            ]
        }

        # Als line 7 niet werkt met objectpath
        _user_data = {
            'persoon': {
                'geboortedatum': '1950-01-01T00:00:00Z'
            },
            'foo': _test_data
        }

        self.test_data = objectpath.Tree(_test_data)
        self.user_data = objectpath.Tree(_user_data)
    def test_apply_rules_simple(self):
        rules = [
            {"type": "rule", "rule": "2 > 1"}
        ]
        compound_rules = {}

        self.assertTrue(apply_rules(self.test_data, rules, compound_rules))

        rules = [
            {"type": "rule", "rule": "2 > 1"},
            {"type": "rule", "rule": "false"},
        ]
        self.assertFalse(apply_rules(self.test_data, rules, compound_rules))

    def test_apply_rules_nested(self):
        compound_rules = {
            "1": {
                "name": "rule 1",
                "rules": [
                    {"type": "rule", "rule": "true"}
                ]
            },
            "2": {
                "name": "rule 2",
                "rules": [
                    {"type": "ref", "ref_id": "1"}
                ]
            }
        }
        
        rules = [
            {"type": "ref", "ref_id": "1"}
        ]
        self.assertTrue(apply_rules(self.test_data, rules, compound_rules))

        rules = [
            {"type": "ref", "ref_id": "1"}
        ]
        self.assertTrue(apply_rules(self.test_data, rules, compound_rules))

    def test_apply_rules_recursing(self):
        compound_rules = {
            "1": {
                "name": "rule 1",
                "rules": [
                    {"type": "ref", "ref_id": "2"}
                ]
            },
            "2": {
                "name": "rule 2",
                "rules": [
                    {"type": "ref", "ref_id": "1"}
                ]
            }
        }
        rules = [{"type": "ref", "ref_id": "1"}]
        with self.assertRaises(RecursionError):
            apply_rules(self.test_data, rules, compound_rules)

        # self referencing
        compound_rules = {
            "1": {
                "name": "rule 1",
                "rules": [
                    {"type": "ref", "ref_id": "1"}
                ]
            }
        }
        rules = [{"type": "ref", "ref_id": "1"}]
        with self.assertRaises(RecursionError):
            apply_rules(self.test_data, rules, compound_rules)

    def test_stadspas(self):
        fixture = get_fixture()
        user_data = objectpath.Tree(fixture["data"])
        rules = [
            {"type": "ref", "ref_id": "1"} # ID 1 is the stadspas rule
        ]
        print(user_data.execute("$.focus.*[@.soortProduct is 'Minimafonds' and @.typeBesluit is 'Toekenning']"))
        self.assertTrue(apply_rules(user_data, rules, compound_rules))
        # Change birth date so test will assert differently
        fixture["data"]['focus'][0]['soortProduct'] = 'Participatiewet'
        user_data = objectpath.Tree(fixture["data"])
        self.assertFalse(apply_rules(user_data, rules, compound_rules))

    #This test works
    def test_is_18(self):
        fixture = get_fixture()
        user_data = objectpath.Tree(fixture["data"])
        rules = [
            {"type": "ref", "ref_id": "2"} 
        ]
        self.assertTrue(apply_rules(user_data, rules, compound_rules))
        
        # Change birth date so test will assert differently
        fixture["data"]['brp']['persoon']['geboortedatum'] = '2002-01-01T00:00:00Z'
        user_data = objectpath.Tree(fixture["data"])
        self.assertTrue(apply_rules(user_data, rules, compound_rules))

        fixture["data"]['brp']['persoon']['geboortedatum'] = '2018-01-01T00:00:00Z'
        user_data = objectpath.Tree(fixture["data"])
        self.assertFalse(apply_rules(user_data, rules, compound_rules))
 
    #This test works
    def test_woont_in_gemeente_Amsterdam(self):
        fixture = get_fixture()
        user_data = objectpath.Tree(fixture["data"])
        rules = [
            {"type": "ref", "ref_id": "3"} 
        ]
        self.assertTrue(apply_rules(user_data, rules, compound_rules))

        fixture["data"]['brp']['persoon']['mokum'] = True
        user_data = objectpath.Tree(fixture["data"])
        self.assertTrue(apply_rules(user_data, rules, compound_rules))

        # Change birth date so test will assert differently
        fixture["data"]['brp']['persoon']['mokum'] = False
        user_data = objectpath.Tree(fixture["data"])
        self.assertFalse(apply_rules(user_data, rules, compound_rules))


    def test_heeft_kinderen(self):
        fixture = get_fixture()
        user_data = objectpath.Tree(fixture["data"])
        rules = [
            {"type": "ref", "ref_id": "4"}
        ]
        self.assertTrue(apply_rules(user_data, rules, compound_rules))
        # Change birth date so test will assert differently
        fixture["data"]['brp']['kinderen'] = []
        print("HSHDNEND", fixture['data']['brp'])
        user_data = objectpath.Tree(fixture["data"])
        self.assertFalse(apply_rules(user_data, rules, compound_rules))

    #This test works
    def test_is_ingeschreven_in_Amsterdam(self):
        fixture = get_fixture()
        user_data = objectpath.Tree(fixture["data"])
        rules = [
            {"type": "ref", "ref_id": "5"}
        ]
        self.assertTrue(apply_rules(user_data, rules, compound_rules))

        fixture["data"]['brp']['persoon']['geboortedatum'] = 'Amsterdam'
        user_data = objectpath.Tree(fixture["data"])
        self.assertTrue(apply_rules(user_data, rules, compound_rules))

        # Change birth date so test will assert differently
        fixture["data"]['brp']['persoon']['gemeentenaamInschrijving'] = 'Utrecht'
        user_data = objectpath.Tree(fixture["data"])
        self.assertFalse(apply_rules(user_data, rules, compound_rules))

    def test_kind_is_tussen_2_en_18_jaar(self):
        fixture = get_fixture()
        user_data = objectpath.Tree(fixture["data"])
        rules = [
            {"type": "ref", "ref_id": "6"}
        ]
        self.assertFalse(apply_rules(user_data, rules, compound_rules))
        # Change birth date so test will assert differently
        fixture["data"]['brp']['kinderen'][0]['geboortedatum'] = '2012-01-01T00:00:00Z'
        user_data = objectpath.Tree(fixture["data"])
        self.assertTrue(apply_rules(user_data, rules, compound_rules))

    def test_kind_is_op_30_september_2020_geen_18(self):
        fixture = get_fixture()
        user_data = objectpath.Tree(fixture["data"])
        rules = [
            {"type": "ref", "ref_id": "7"}
        ]
        self.assertTrue(apply_rules(user_data, rules, compound_rules))
        # Change birth date so test will assert differently
        fixture["data"]['brp']['persoon']['geboortedatum'] = '2012-01-01T00:00:00Z'
        user_data = objectpath.Tree(fixture["data"])
        self.assertFalse(apply_rules(user_data, rules, compound_rules))