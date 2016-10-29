from setuptools import setup
from setuptools.command.test import test as TestCommand
import loris
import sys

# Distribution Guidance:
# https://www.digitalocean.com/community/tutorials/how-to-package-and-distribute-python-applications
# https://docs.python.org/3/distutils/sourcedist.html
# http://python-packaging.readthedocs.io/en/latest/minimal.html
# Maybe for init script? http://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-console-scripts-entry-point

class PyTest(TestCommand):
    # TODO: figure out how to get the stuff we have in setup.cfg into this
    # class instead, if possible, or else get rid of this so that config is all
    # in one place. See:
    # http://pytest.org/latest/goodpractices.html#manual-integration
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        self.pytest_args.insert(0, '--cache-clear')
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

PACKAGES=(
    'loris',
    'loris.compliance',
    'loris.handlers',
    'loris.helpers',
    'loris.info',
    'loris.parameters',
    'loris.resolvers',
    'loris.transcoders',
)

PACKAGE_DATA={
    'loris': ['sample.jp2','config.json'],
    'loris.www': ['www/favicon.ico'],
    'loris.openjpeg': [
        'openjpeg/linux/x86_64/opj_decompress',
        'openjpeg/linux/x86_64/libopenjp2.so.2.1.2'
    ]
}

setup(
    name='Loris',
    version=loris.__version__,
    author='Jon Stroop',
    author_email='jpstroop@gmail.com',
    packages=PACKAGES,
    # Include additional files into the package
    package_data=PACKAGE_DATA,
    include_package_data=True,
    # Details
    #url='http://pypi.python.org/pypi/MyApplication_v010/',
    license='LICENSE.txt',
    description='Loris IIIF Image Server',
    long_description=open('README.md').read(),
    cmdclass = {'test': PyTest},
    setup_requires=[ ],
    tests_require=[
        'nose==1.3.7',
        'pytest==3.0.3'
    ],
    install_requires=[
        'CherryPy==8.1.2',
        'Pillow==3.4.2',
        'python-magic==0.4.12',
        'requests==2.11.1',
    ]
)
