from setuptools import setup
from boxmath import __version__

try:
    from setuptools.command.test import test
except ImportError:
    cmdclass = {}
else:
    class pytest(test):

        def finalize_options(self):
            test.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            from pytest import main
            errno = main(self.test_args)
            raise SystemExit(errno)
    cmdclass = {'test': pytest}

setup(
    name="boxmath",
    version=__version__,
    description="Simple image box arithmatic",
    packages=["boxmath"],
    tests_require=["pytest", "pytest-quickcheck"],
    cmdclass=cmdclass
)
