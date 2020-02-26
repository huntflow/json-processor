import unittest
from json_processor import json_process


class BaseTest(unittest.TestCase):
    def test_simple_return(self):
        self.assertEqual(json_process('Hello, world!', {}), 'Hello, world!')
        self.assertEqual(json_process({'a': 1}, {}), {'a': 1})
        self.assertEqual(json_process({'type': 'object', 'value': {'id': 1}}, {}), {'id': 1})

    def test_unsupported(self):
        self.assertRaises(Exception, json_process, {'type': 'unsupported'}, {})
