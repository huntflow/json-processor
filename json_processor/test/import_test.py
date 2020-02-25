# flake8: noqa
import subprocess
import sys
import unittest

_import_everything = b"""
import json_processor
import json_processor.version
"""


class ImportTest(unittest.TestCase):
    def test_import_everything(self):
        # Test that all Torn modules can be imported without side effects,
        # specifically without initializing the default asyncio event loop.
        # Since we can't tell which modules may have already beein imported
        # in our process, do it in a subprocess for a clean slate.
        proc = subprocess.Popen([sys.executable], stdin=subprocess.PIPE)
        proc.communicate(_import_everything)
        self.assertEqual(proc.returncode, 0)
