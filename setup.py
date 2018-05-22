#!/usr/bin/env python

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='nagios_registration',
    version='1.0',
    packages=['nagios_registration'],
    include_package_data=True,
    install_requires = [
        'Django==1.11.10',
        'django-templatetag-handlebars==1.3.0',
    ],
    license='Apache License, Version 2.0',
    description='An application that registers hosts for Nagios monitoring',
    long_description=README,
    url='https://github.com/uw-it-aca/nagios_registration',
    author = "UW-IT AXDD",
    author_email = "aca-it@uw.edu",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)
