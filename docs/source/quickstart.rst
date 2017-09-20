Quickstart
==========

Requirements
------------
* Python 2.7+
* Python 3.4+
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
