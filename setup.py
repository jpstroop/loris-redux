from setuptools import setup
from setuptools.command.test import test as TestCommand
import loris
import sys

class PyTest(TestCommand):
    # TODO: figure out how to get the stuff we have in setup.cfg into this
    # class instead. See:
    # http://pytest.org/latest/goodpractices.html#manual-integration
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='Loris',
    version=loris.__version__,
    author='Jon Stroop',
    author_email='jpstroop@gmail.com',
    packages=['loris'],
    # Include additional files into the package
    include_package_data=True,
    # Details
    #url='http://pypi.python.org/pypi/MyApplication_v010/',
    license='LICENSE.txt',
    description='Loris IIIF Image Server',
    long_description=open('README.md').read(),
    cmdclass = {'test': PyTest},
    setup_requires=[ ],
    tests_require=[
        'pytest==2.9.1'
    ],
    install_requires=[
        'Pillow==3.2.0',
        'tornado==4.3',
    ],
)
