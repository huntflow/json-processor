import unittest
from json_processor import json_process


class ArrayTest(unittest.TestCase):
    def test_array(self):
        self.assertListEqual(json_process({
            'type': 'array',
            'from': {
                'type': 'jsonpointer',
                'value': '/data/items'
            },
            'value': {
                'type': 'object',
                'value': {
                    'id': {
                        'type': 'jsonpointer',
                        'value': '/$value/foreign'
                    },
                    'name': {
                        'type': 'jsonpointer',
                        'value': '/$value/name'
                    },
                    'index': {
                        'type': 'jsonpointer',
                        'value': '/$index0'
                    }
                }
            }
        }, {
            'data': {
                'items': [
                    {'foreign': '100', 'name': 'item1'},
                    {'foreign': '150', 'name': 'item2'}
                ]
            }
        }), [{'id': '100', 'name': 'item1', 'index': 0}, {'id': '150', 'name': 'item2', 'index': 1}])
