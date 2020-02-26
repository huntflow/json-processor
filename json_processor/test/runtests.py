import io
import logging
import textwrap
import sys
import unittest
import warnings


if sys.version_info >= (3,):
    # On python 3, mixing unittest2 and unittest (including doctest)
    # doesn't seem to work, so always use unittest.
    import unittest
else:
    # On python 2, prefer unittest2 when available.
    try:
        import unittest2 as unittest  # type: ignore
    except ImportError:
        import unittest  # type: ignore


TEST_MODULES = [
    'json_processor.test.import_test',
    'json_processor.test.base_test',
    'json_processor.test.cast_test',
    'json_processor.test.array_test',
]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)


def test_runner_factory(stderr):
    class JSONProcessorTextTestRunner(unittest.TextTestRunner):
        def __init__(self, *args, **kwargs):
            kwargs['stream'] = stderr
            super(JSONProcessorTextTestRunner, self).__init__(*args, **kwargs)

        def run(self, test):
            result = super(JSONProcessorTextTestRunner, self).run(test)
            if result.skipped:
                skip_reasons = set(reason for (test, reason) in result.skipped)
                self.stream.write(
                    textwrap.fill(
                        'Some tests were skipped because: %s'
                        % ', '.join(sorted(skip_reasons))
                    )
                )
                self.stream.write('\n')
            return result

    return JSONProcessorTextTestRunner


class CountingStderr(io.IOBase):
    def __init__(self, real):
        self.real = real
        self.byte_count = 0

    def write(self, data):
        self.byte_count += len(data)
        return self.real.write(data)

    def flush(self):
        return self.real.flush()


def main():
    # Be strict about most warnings (This is set in our test running
    # scripts to catch import-time warnings, but set it again here to
    # be sure). This also turns on warnings that are ignored by
    # default, including DeprecationWarnings and python 3.2's
    # ResourceWarnings.
    warnings.filterwarnings('error')
    # setuptools sometimes gives ImportWarnings about things that are on
    # sys.path even if they're not being used.
    warnings.filterwarnings('ignore', category=ImportWarning)
    # json-processor generally shouldn't use anything deprecated, but some of
    # our dependencies do (last match wins).
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    warnings.filterwarnings('error', category=DeprecationWarning, module=r'json_processor\..*')
    warnings.filterwarnings('ignore', category=PendingDeprecationWarning)
    warnings.filterwarnings(
        'error', category=PendingDeprecationWarning, module=r'json_processor\..*'
    )

    # Certain errors (especially 'unclosed resource' errors raised in
    # destructors) go directly to stderr instead of logging. Count
    # anything written by anything but the test runner as an error.
    orig_stderr = sys.stderr
    counting_stderr = CountingStderr(orig_stderr)
    sys.stderr = counting_stderr  # type: ignore

    kwargs = {}
    kwargs['testRunner'] = test_runner_factory(orig_stderr)
    argv = sys.argv

    try:
        # In order to be able to run tests by their fully-qualified name
        # on the command line without importing all tests here,
        # module must be set to None.  Python 3.2's unittest.main ignores
        # defaultTest if no module is given (it tries to do its own
        # test discovery, which is incompatible with auto2to3), so don't
        # set module if we're not asking for a specific test.
        if len(argv) > 1:
            unittest.main(module=None, argv=argv, **kwargs)
        else:
            unittest.main(defaultTest='all', argv=argv, **kwargs)
    except SystemExit as e:
        if e.code == 0:
            logging.info('PASS')
        else:
            logging.error('FAIL')
        raise


if __name__ == '__main__':
    main()
