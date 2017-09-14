#!/usr/bin/env python
from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'gyazo/__about__.py')) as f:
    exec(f.read())

install_requires = [
    'python-dateutil>=2.4.2',
    'requests>=2.7.0',
    'six>=1.9.0',
]

extras_require = {
    ':python_version<"3.5"': [
        'typing',
    ],
    'docs': [
        'Sphinx>=1.4,<1.5',
        'sphinx_rtd_theme<0.2,>=0.1.9',
    ],
    'test': [
        'coverage>=4.3.4,<5.0.0',
        'coveralls>=1.1,<2.0',
        'flake8>=3.3.0,<4.0.0',
    ],
    'test:python_version < "3.3"': [
        'mock>=2.0.0,<3.0.0',
    ],
    'test:python_version >= "3.3"': [
        'mypy',
    ],
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
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='python-gyazo',
    version=__version__,
    description='A Python wrapper for Gyazo API',
    long_description=long_description,
    author='Yusuke Miyazaki',
    author_email='miyazaki.dev@gmail.com',
    url='https://github.com/ymyzk/python-gyazo',
    license='MIT',
    packages=['gyazo'],
    test_suite='tests',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=classifiers,
)
