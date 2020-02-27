import json
import sys
import warnings

from json_processor import json_process


def main():
    warnings.simplefilter('ignore', DeprecationWarning)

    argv = sys.argv
    if len(argv) < 3:
        print('Not enough parameters to run.')
        print('usage:\tjson_process schema_file json_file')
        sys.exit(-1)

    with open(argv[1], 'r') as f:
        schema = json.loads(f.read())

    with open(argv[2], 'r') as fd:
        data = json.loads(fd.read())

    print(json.dumps(json_process(schema, data), ensure_ascii=False))


if __name__ == '__main__':
    main()
