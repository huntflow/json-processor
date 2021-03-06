from copy import deepcopy

from jsonpointer import resolve_pointer

from .version import version


__version__ = version


class PopException(BaseException):
    pass


def nothing(value):
    return value


def try_int(value, default=None):
    try:
        return int(value)
    except:
        return default


def null_if_empty(value):
    if isinstance(value, dict):
        has_any = any(map(lambda x: x is not None, value.values()))
        return value if has_any else None
    elif isinstance(value, list):
        return None if len(value) == 0 else value

    return value


def pop_if_empty(value):
    if null_if_empty(value) is None:
        raise PopException()

    return value


_CAST_TYPES = {
    'integer': try_int,
    'null_if_empty': null_if_empty,
    'pop_if_empty': pop_if_empty,
    None: nothing
}


def json_process(schema, data):
    if isinstance(schema, list):
        return [json_process(x, data) for x in schema]

    if not isinstance(schema, dict):
        return schema

    if not schema.get('type'):
        return schema

    schema_type = schema['type']

    if schema_type == 'object':
        result = {}
        for key, value in schema['value'].items():
            try:
                result[key] = _CAST_TYPES[schema.get('cast')](json_process(value, data))
            except PopException:
                continue

        return _CAST_TYPES[schema.get('cast')](result)
    elif schema_type == 'jsonpointer':
        return _CAST_TYPES[schema.get('cast')](resolve_pointer(data, schema['value'], None))
    elif schema_type == 'array':
        values = json_process(schema['from'], data)
        new_data = deepcopy(data)
        result = []

        if values:
            for index, value in enumerate(values):
                new_data['$index0'] = index
                new_data['$value'] = value
                result.append(json_process(schema['value'], new_data))

        return _CAST_TYPES[schema.get('cast')](result)
    else:
        raise Exception('Unexpected type {}'.format(schema_type))
