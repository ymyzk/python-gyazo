#!/usr/bin/env python
from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'python-dateutil>=2.4.2',
    'requests>=2.7.0',
    'six>=1.9.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.4,<1.5',
        'sphinx_rtd_theme<0.2,>=0.1.9',
    ]
}

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='python-gyazo',
    version='0.12.0',
    description='A Python wrapper for Gyazo API',
    long_description=long_description,
    author='Yusuke Miyazaki',
    author_email='miyazaki.dev@gmail.com',
    url='https://github.com/ymyzk/python-gyazo',
    license='MIT',
    packages=['gyazo'],
    test_suite='tests',
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=classifiers,
)
