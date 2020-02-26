import unittest
from json_processor import json_process


class CastTest(unittest.TestCase):
    def test_cast_int(self):
        self.assertEqual(json_process({'type': 'object', 'value': {'id': '1', 'cast': 'integer'}}, {}), {'id': 1})
        self.assertEqual(json_process({'type': 'object', 'value': {'id': '1.0', 'cast': 'integer'}}, {}), {'id': 1})
        self.assertEqual(json_process({'type': 'object', 'value': {'id': '-1', 'cast': 'integer'}}, {}), {'id': -1})
