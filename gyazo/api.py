#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import requests
import six

from .error import GyazoError
from .image import Image, ImageList


class Api(object):
    """A Python interface for Gyazo API"""

    def __init__(self, client_id=None, client_secret=None, access_token=None,
                 api_url='https://api.gyazo.com',
                 upload_url='https://upload.gyazo.com'):
        """
        :param client_id: API client ID
        :type client_id: str | unicode
        :param client_secret: API secret
        :type client_secret: str | unicode
        :param access_token: API access token
        :type access_token: str | unicode
        :param api_url: (optional) API endpoint URL
                        (default: https://api.gyazo.com)
        :type api_url: str | unicode
        :param upload_url: (optional) Upload API endpoint URL
                        (default: https://upload.gyazo.com)
        :type upload_url: str | unicode
        """
        self.api_url = api_url
        self.upload_url = upload_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = access_token

    def get_image_list(self, page=1, per_page=20):
        """Return a list of user's saved images

        :param int page: (optional) Page number (default: 1)
        :param int per_page: (optional) Number of images per page
                             (default: 20, min: 1, max 100)
        :rtype: ImageList
        """
        url = self.api_url + '/api/images'
        parameters = {
            'page': page,
            'per_page': per_page
        }
        response = self._request_url(
            url, 'get', parameters, with_access_token=True)
        headers, result = self._parse_and_check(response)
        images = ImageList.from_list(result)
        images.set_attributes_from_headers(headers)
        return images

    def upload_image(self, image_file):
        """Upload an image

        :param image_file: File-like object of an image file
        :type image_file: file object
        :rtype: Image
        """
        url = self.upload_url + '/api/upload'
        files = {
            'imagedata': image_file
        }
        response = self._request_url(
            url, 'post', files=files, with_access_token=True)
        headers, result = self._parse_and_check(response)
        return Image.from_dict(result)

    def delete_image(self, image_id):
        """Delete an image

        :param image_id: Image ID
        :type image_id: str | unicode
        :rtype: Image
        """
        url = self.api_url + '/api/images/' + image_id
        response = self._request_url(url, 'delete', with_access_token=True)
        headers, result = self._parse_and_check(response)
        return Image.from_dict(result)

    def get_oembed(self, url):
        """Return an oEmbed format json dictionary

        :param url: Image page URL (ex. http://gyazo.com/xxxxx)
        :type url: str | unicode
        :rtype: dict
        """
        api_url = self.api_url + '/api/oembed'
        parameters = {
            'url': url
        }
        response = self._request_url(api_url, 'get', parameters)
        headers, result = self._parse_and_check(response)
        return result

    def _request_url(self, url, method, data=None, files=None,
                     with_client_id=False, with_access_token=False):
        """Send HTTP request

        :param url: URL
        :type url: str | unicode
        :param method: HTTP method (get, post or delete)
        :type method: str | unicode
        :param with_client_id: send request with client_id (default: false)
        :type with_client_id: bool
        :param with_access_token: send request with with_access_token
                                  (default: false)
        :type with_access_token: bool
        :raise GyazoError:
        """
        headers = {}
        if data is None:
            data = {}

        if with_client_id and self._client_id is not None:
            data['client_id'] = self._client_id

        if with_access_token and self._access_token is not None:
            data['access_token'] = self._access_token

        if method == 'get':
            try:
                return requests.get(url, data=data, headers=headers)
            except requests.RequestException as e:
                raise GyazoError(six.text_type(e))
        elif method == 'post':
            try:
                return requests.post(url, data=data, files=files,
                                     headers=headers)
            except requests.RequestException as e:
                raise GyazoError(six.text_type(e))
        elif method == 'delete':
            try:
                return requests.delete(url, data=data, headers=headers)
            except requests.RequestException as e:
                raise GyazoError(six.text_type(e))

        # Unsupported method
        return None

    def _parse_and_check(self, data):
        try:
            headers = data.headers
            json_data = data.json()
        except Exception as e:
            raise e

        if data.status_code >= 400:
            message = json_data.get('message', 'Error')
            raise GyazoError(message)

        return headers, json_data
