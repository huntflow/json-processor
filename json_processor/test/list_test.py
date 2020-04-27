import unittest
from json_processor import json_process


class ListTest(unittest.TestCase):
    def test_list(self):
        self.assertListEqual(json_process({
            'type': 'array',
            'from': [1, 2, 3],
            'value': {
                'type': 'jsonpointer',
                'value': '/$value'
            }
        }, {}), [1, 2, 3])

    def test_more_complex(self):
        self.assertListEqual(json_process({
            'type': 'array',
            'from': [
                {'type': 'jsonpointer', 'value': '/data/test_field'},
                3,
                {'type': 'jsonpointer', 'value': '/data/test'}
            ],
            'value': {
                'type': 'object',
                'value': {
                    'field': {
                        'type': 'jsonpointer',
                        'value': '/$value'
                    }
                }
            }
        }, {
            'data': {
                'test_field': 'Hello',
                'test': 'World',
            }
        }), [{'field': 'Hello'}, {'field': 3}, {'field': 'World'}])
