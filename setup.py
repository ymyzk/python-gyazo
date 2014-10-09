#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


__author__ = 'Yusuke Miyazaki <miyazaki.dev@gmail.com>'
__version__ = '0.3.0'

requires = [
    'requests>=2.4.0',
    'python-dateutil>=2.2'
]

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

setup(name='python-gyazo',
      version=__version__,
      description='A Python wrapper for Gyazo API',
      author=__author__,
      author_email='miyazaki.dev@gmail.com',
      url='https://github.com/ymyzk/python-gyazo',
      packages=['gyazo'],
      test_suite='tests',
      install_requires=requires,
      classifiers=classifiers)