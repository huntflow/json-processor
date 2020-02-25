from copy import deepcopy

from jsonpointer import resolve_pointer

from .version import version


__version__ = version


def nothing(x):
    return x


_CAST_TYPES = {
    'integer': int,
    None: nothing
}


def json_process(schema, data):
    if not isinstance(schema, dict):
        return schema

    if not schema.get('type'):
        return schema

    schema_type = schema['type']

    if schema_type == 'object':
        result = {}
        for key, value in schema['value'].items():
            result[key] = _CAST_TYPES[schema.get('cast')](json_process(value, data))

        return result
    elif schema_type == 'jsonpointer':
        return _CAST_TYPES[schema.get('cast')](resolve_pointer(data, schema['value']))
    elif schema_type == 'array':
        values = json_process(schema['from'], data)
        new_data = deepcopy(data)
        result = []
        for index, value in enumerate(values):
            new_data['$index0'] = index
            new_data['$value'] = value
            result.append(json_process(schema['value'], new_data))

        return result
    else:
        raise Exception('Unexpected type {}'.format(schema_type))
