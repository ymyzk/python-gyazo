# python-gyazo
[![PyPI version](https://badge.fury.io/py/python-gyazo.svg)](http://badge.fury.io/py/python-gyazo)

A Python wrapper for Gyazo API.

## Requirements
* Python 2.7
* Python 3.4

## Installation
`pip install python-gyazo`

## Usage
Create application and get access token from https://gyazo.com/oauth/applications

```python
from gyazo import Api

api = Api(client_id='YOUR_CLIENT_ID',
          client_secret='YOUR_CLIENT_SECRET',
          access_token='YOUR_ACCESS_TOKEN')

# Get image list
images = api.get_image_list()
for image in images:
    print(str(image))

# Using image model
image = images[0]
print("Image ID: " + image.image_id)
print("URL: " + image.url)

# Delete image
api.delete_image('IMAGE_ID')
```

## Known issues
* Uploading images is not supported.

## Links
* [Gyazo API](https://gyazo.com/api/docs)
