#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from distutils.core import setup


setup(name='python-gyazo',
      version='0.2.0',
      description='A Python wrapper for Gyazo API',
      author='Yusuke Miyazaki',
      author_email='miyazaki.dev@gmail.com',
      url='https://github.com/litesystems/python-gyazo',
      packages=['gyazo'],
      test_suite='tests',
      install_requires=[
          'requests>=2.3.0',
          'python-dateutil>=2.2'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: Internet',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ]
      )
