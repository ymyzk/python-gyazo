#!/usr/bin/env python

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


__author__ = 'Yusuke Miyazaki <miyazaki.dev@gmail.com>'
__version__ = '0.6.0'

requires = [
    'Jinja2>=2.7.0',
    'progress>=1.2',
    'python-dateutil>=2.4',
    'requests>=2.5.0',
    'six>=1.9.0'
]

if sys.version_info < (3, 2):
    requires.append('futures>=2.2.0')

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
]

setup(name='python-gyazo',
      version=__version__,
      description='A Python wrapper for Gyazo API',
      author=__author__,
      author_email='miyazaki.dev@gmail.com',
      url='https://github.com/ymyzk/python-gyazo',
      packages=['gyazo'],
      package_data={'gyazo': ['themes/default/*']},
      scripts=['scripts/gyazo-backup'],
      test_suite='tests',
      install_requires=requires,
      classifiers=classifiers)
