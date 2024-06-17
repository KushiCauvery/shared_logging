# shared_logging/setup.py

from setuptools import setup

setup(
    name='shared_logging',
    version='0.2',
    packages=['shared_logging'],
    install_requires=[
        'django',
        'djangorestframework',
        # Add any other dependencies as needed for the project
    ],
)
