python-gyazo
============
.. image:: https://badge.fury.io/py/python-gyazo.svg
   :target: https://pypi.python.org/pypi/python-gyazo/
   :alt: PyPI version
.. image:: https://img.shields.io/pypi/dm/python-gyazo.svg
   :target: https://pypi.python.org/pypi/python-gyazo/
   :alt: Downloads
.. image:: https://travis-ci.org/ymyzk/python-gyazo.svg?branch=master
   :target: https://travis-ci.org/ymyzk/python-gyazo
   :alt: Build Status
.. image:: https://readthedocs.org/projects/python-gyazo/badge/?version=latest
   :target: https://python-gyazo.readthedocs.io/
   :alt: Documentation Status
.. image:: https://codeclimate.com/github/ymyzk/python-gyazo/badges/gpa.svg
   :target: https://codeclimate.com/github/ymyzk/python-gyazo
   :alt: Code Climate
.. image:: https://coveralls.io/repos/ymyzk/python-gyazo/badge.svg?branch=master
   :target: https://coveralls.io/r/ymyzk/python-gyazo?branch=master
   :alt: Coverage Status

A Python wrapper for Gyazo API.

The full-documentation is available on `Read the Docs`_.

Requirements
------------
* Python 2.7+
* Python 3.3+
* PyPy
* PyPy3

Installation
------------
.. code-block:: shell

   pip install python-gyazo

Usage
-----
At first, you must create an application and get an access token from https://gyazo.com/oauth/applications

.. code-block:: python

   from __future__ import print_function

   from gyazo import Api


   api = Api(access_token='YOUR_ACCESS_TOKEN')

   ### Get a list of images
   images = api.get_image_list()
   for image in images:
       print(str(image))

   ### Using an image model
   image = images[0]
   print("Image ID: " + image.image_id)
   print("URL: " + image.url)

   ### Download an image
   if image.url:
       with open(image.filename, 'wb') as f:
           f.write(image.download())

   ### Upload an image
   with open('sample.png', 'rb') as f:
       image = api.upload_image(f)
       print(image.to_json())

   ### Delete an image
   api.delete_image('IMAGE_ID')

   ### oEmbed
   image = images[0]
   print(api.get_oembed(image.permalink_url))

Backup
------
python-gyazo includes a utility program called ``gyazo-backup``.
You can download all images from Gyazo with this command.

.. image:: docs/source/images/backup_example.jpg

For more details, please see `this page`_.

License
-------
MIT License. Please see `LICENSE`_.

.. _Read the Docs: https://python-gyazo.readthedocs.io/
.. _this page: https://python-gyazo.readthedocs.io/en/stable/backup.html
.. _LICENSE: LICENSE
