python-gyazo
============
.. image:: https://badge.fury.io/py/python-gyazo.svg
   :target: https://pypi.python.org/pypi/python-gyazo/
   :alt: PyPI version
.. image:: https://img.shields.io/pypi/pyversions/python-gyazo.svg
   :target: https://pypi.python.org/pypi/python-gyazo/
   :alt: PyPI Python versions
.. image:: https://github.com/ymyzk/python-gyazo/workflows/CI/badge.svg
   :target: https://github.com/ymyzk/python-gyazo/actions?query=workflow%3ACI
   :alt: CI Status
.. image:: https://readthedocs.org/projects/python-gyazo/badge/?version=latest
   :target: https://python-gyazo.readthedocs.io/
   :alt: Documentation Status

A Python wrapper for `Gyazo API`_.

The full-documentation is available on `Read the Docs`_.

Requirements
------------
* Python 3.5+

Installation
------------
.. code-block:: shell

   pip install python-gyazo

Note: Please use the latest version of setuptools & pip

.. code-block:: shell

   pip install -U setuptools pip


Usage
-----
At first, you must create an application and get an access token from https://gyazo.com/oauth/applications

.. code-block:: python

   from gyazo import Api


   client = Api(access_token='YOUR_ACCESS_TOKEN')

   ### Get a list of images
   images = client.get_image_list()
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
       image = client.upload_image(f)
       print(image.to_json())

   ### Delete an image
   client.delete_image('IMAGE_ID')

   ### oEmbed
   image = images[0]
   print(client.get_oembed(image.permalink_url))

Backup
------
``gyazo-backup`` is moved to `python-gyazo-backup`_.

License
-------
MIT License. Please see `LICENSE`_.

.. _Read the Docs: https://python-gyazo.readthedocs.io/
.. _Gyazo API: https://gyazo.com/api?lang=ja
.. _python-gyazo-backup: https://github.com/ymyzk/python-gyazo-backup
.. _LICENSE: LICENSE
