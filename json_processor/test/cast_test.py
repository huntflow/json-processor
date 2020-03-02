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

        self.assertEqual(json_process({'type': 'object', 'value': {
            'id': {
                'type': 'jsonpointer',
                'value': '/id',
                'cast': 'integer'
            }
        }}, {'id': None}), {'id': None})

    def test_cast_null_if_empty(self):
        self.assertEqual(json_process({'type': 'object', 'value': {
            'id': {
                'type': 'jsonpointer',
                'value': '/id'
            }
        }, 'cast': 'null_if_empty'}, {'id': 1}), {'id': 1})

        self.assertEqual(json_process({'type': 'object', 'value': {
            'id': {
                'type': 'jsonpointer',
                'value': '/id'
            }
        }, 'cast': 'null_if_empty'}, {'id': None}), None)

        self.assertEqual(json_process({'type': 'object', 'value': {
            'value': {
                'type': 'object',
                'value': {
                    'id': {
                        'type': 'jsonpointer',
                        'value': '/id'
                    }
                },
                'cast': 'null_if_empty'
            }
        }}, {'id': None}), {'value': None})

        self.assertEqual(json_process({'type': 'object', 'value': {
            'value': {
                'type': 'object',
                'value': {
                    'id': {
                        'type': 'jsonpointer',
                        'value': '/id'
                    }
                },
                'cast': 'null_if_empty'
            }
        }, 'cast': 'null_if_empty'}, {'id': None}), None)

        self.assertEqual(json_process({'type': 'array', 'from': [], 'value': {
            'id': {
                'type': 'jsonpointer',
                'value': '/id'
            }
        }, 'cast': 'null_if_empty'}, {}), None)

        self.assertEqual(json_process({'type': 'object', 'value': {
            'id': {
                'type': 'jsonpointer',
                'value': '/id',
                'cast': 'null_if_empty'
            }
        }}, {'id': None}), {'id': None})

        self.assertEqual(json_process({'type': 'object', 'value': {
            'id': {
                'type': 'jsonpointer',
                'value': '/id',
                'cast': 'null_if_empty'
            }
        }}, {'id': False}), {'id': False})

        self.assertEqual(json_process({'type': 'object', 'value': {
            'id': {
                'type': 'jsonpointer',
                'value': '/id',
                'cast': 'null_if_empty'
            }
        }}, {'id': 0}), {'id': 0})

    def test_cast_pop_if_empty(self):
        self.assertEqual(json_process({'type': 'object', 'value': {
            'data': {
                'type': 'object',
                'value': {
                    'id': {
                        'type': 'jsonpointer',
                        'value': '/id'
                    }
                },
                'cast': 'pop_if_empty'
            },
            'flag': True
        }}, {'id': None}), {'flag': True})
