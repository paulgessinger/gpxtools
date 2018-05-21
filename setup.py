from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gpxutil',
    version='0.1.0',
    description='Utilities for GPX files and photos',
    url='https://github.com/paulgessinger/gpxutil',
    license='MIT',

    author='Paul Gessinger',

    author_email='hello@paulgessinger.com',

    packages=find_packages(exclude=[]),
    # package_data={
        # 'codereport': ['templates/*'],
    # },

    entry_points = {
        'console_scripts': ["gpxutil=gpxutil.cli:main"]
    },

    install_requires=['pillow', 'gpxpy'],
    tests_require = ['pytest', 'mock']
)
