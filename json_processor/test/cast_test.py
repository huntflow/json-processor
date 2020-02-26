import unittest
from json_processor import json_process


class CastTest(unittest.TestCase):
    def test_cast_int(self):
        self.assertEqual(json_process({'type': 'object', 'value': {
            'id': {
                'type': 'jsonpointer',
                'value': '/id',
                'cast': 'integer'
            }
        }}, {'id': '1'}), {'id': 1})

        self.assertEqual(json_process({'type': 'object', 'value': {
            'id': {
                'type': 'jsonpointer',
                'value': '/id',
                'cast': 'integer'
            }
        }}, {'id': '-1'}), {'id': -1})
