from distutils.core import setup

setup(
    # Application name:
    name='Loris',

    # Version number (initial):
    version='0.0.1',

    # Application author details:
    author='Jon Stroop',
    author_email='jpstroop@gmail.com',

    # Packages
    packages=['app'],

    # Include additional files into the package
    include_package_data=True,

    # Details
    #url='http://pypi.python.org/pypi/MyApplication_v010/',

    #
    license='LICENSE.txt',
    description='Loris IIIF Image Server',
    long_description=open('README.md').read(),

    # Dependent packages (distributions)
    install_requires=[
        'tornado==4.3',
        'pytest==2.9.1'
    ],
)
