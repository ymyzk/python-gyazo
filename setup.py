#!/usr/bin/env python
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


__author__ = 'Yusuke Miyazaki <miyazaki.dev@gmail.com>'
__version__ = '0.10.0'

install_requires = [
    'Jinja2>=2.8',
    'progress>=1.2',
    'python-dateutil>=2.4.2',
    'requests>=2.7.0',
    'six>=1.9.0'
]

if not 'bdist_wheel' in sys.argv:
    if sys.version_info < (3, 2):
        install_requires.append('futures>=3.0.3')

extras_require = {
    ':python_version=="2.7"': [
        'futures>=3.0.3'
    ],
    'docs': [
        'Sphinx<1.4,>=1.3.1',
        'sphinx-rtd-theme<0.2,>=0.1.8'
    ]
}

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
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
]

setup(name='python-gyazo',
      version=__version__,
      description='A Python wrapper for Gyazo API',
      author='Yusuke Miyazaki',
      author_email='miyazaki.dev@gmail.com',
      url='https://github.com/ymyzk/python-gyazo',
      license='MIT',
      packages=['gyazo'],
      package_data={'gyazo': ['themes/default/*']},
      scripts=['scripts/gyazo-backup'],
      test_suite='tests',
      install_requires=install_requires,
      extras_require=extras_require,
      classifiers=classifiers)
