#!/usr/bin/env python
from setuptools import setup

kwargs = {}

with open('json_processor/version.py') as f:
    ns = {}
    exec(f.read(), ns)
    version = ns['version']

install_requires = ['jsonpointer >= 2.0']


with open('README.rst') as f:
    kwargs['long_description'] = f.read()


python_requires = '>= 2.7'
kwargs['python_requires'] = python_requires

setup(
    name='json_processor',
    version=version,
    description='JSON Processor - Convert one JSON to another',
    url='https://github.com/huntflow/json-processor',
    download_url='https://github.com/huntflow/json-processor/tarball/{}'.format(version),
    packages=['json_processor', 'json_processor.test'],
    install_requires=install_requires,
    entry_points = {
        'console_scripts': ['json_process=json_processor.__main__:main'],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    **kwargs
)
