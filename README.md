# python-gyazo
[![PyPI version](https://badge.fury.io/py/python-gyazo.svg)](http://badge.fury.io/py/python-gyazo)
[![Build Status](https://travis-ci.org/ymyzk/python-gyazo.svg?branch=master)](https://travis-ci.org/ymyzk/python-gyazo)
[![Coverage Status](https://img.shields.io/coveralls/ymyzk/python-gyazo.svg)](https://coveralls.io/r/ymyzk/python-gyazo?branch=master)

A Python wrapper for Gyazo API.

## Requirements
* Python 2.7
* Python 3.4+

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

# Download image
if image.url:
    with open(image.filename, 'wb') as f:
        f.write(image.download())

# Upload image
with open('sample.png', 'rb') as f:
    image = api.upload_image(f)
    print(image.to_json())

# Delete image
api.delete_image('IMAGE_ID')
```

## Links
* [Gyazo API](https://gyazo.com/api/docs)
