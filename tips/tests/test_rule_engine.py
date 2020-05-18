from unittest import TestCase

import objectpath
import json

from tips.generator.rule_engine import apply_rules

from tips.tests.fixtures.fixture import get_fixture

with open("C:/xampp/htdocs/Stage_Amsterdam/mijn-tips-api/tips/api/compound_rules.json") as compound_rules_file:
    compound_rules = json.load(compound_rules_file)


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
        print("HDBHDB", compound_rules)
        stadspas_rule = compound_rules{"1"}
        self.assertTrue(apply_rules(self.test_data, rules, compound_rules))
