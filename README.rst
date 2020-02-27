JSON processor
==============

.. image:: https://travis-ci.org/huntflow/json-processor.svg?branch=master
  :target: https://travis-ci.org/huntflow/json-processor
.. image:: https://codecov.io/gh/huntflow/json-processor/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/huntflow/json-processor


Simply convert one JSON to another.

* **Easy to use.** Create a simple JSON conversion schema and pass it to processor
* **Rich.** It uses ``jsonpointer`` so you can create complex processors


Example
-------

.. code-block:: python

    from json_processor import json_process

    schema = {
        "type": "object",
        "value": {
            "simple_key": "Just a string",
            "values": {
                "type": "array",
                "from": {
                    "type": "jsonpointer",
                    "value": "/data/items"
                },
                "value": {
                    "type": "object",
                    "value": {
                        "id": {
                            "type": "jsonpointer",
                            "value": "/$value/foreign",
                            "cast": "integer"
                        },
                        "name": {
                            "type": "jsonpointer",
                            "value": "/$value/name"
                        }
                    }
                }
            }
        }
    }

    data = {
        "data": {
            "items": [
                {
                    "foreign": "100",
                    "name": "Item 1"
                },
                {
                    "foreign": "150",
                    "name": "Item 2"
                }
            ]
        }
    }

    print(json_process(schema, data))

    # Outputs:
    # {'simple_key': 'Just a string', 'values': [{'id': 100, 'name': 'Item 1'}, {'id': 150, 'name': 'Item 2'}]}


Installation
------------

From PyPi
~~~~~~~~~

.. code-block:: bash

    pip install json_processor


Command line tool
-----------------

After installation you can use ``json_process`` utility:

.. code-block:: bash

    json_process <schema_file> <json_file>
