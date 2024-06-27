from setuptools import setup

setup(
    name='shared_config',
    version='0.1',
    packages=['shared_config'],
    include_package_data=True,  # Ensure package data is included
    install_requires=[
        'django',
        'djangorestframework',
        'pycryptodome',
        'django-environ',
        'pystache',
        'psycopg2',
        # Add any other dependencies as needed for the project
    ],
)
