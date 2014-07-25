#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import requests

from .error import GyazoError
from .image import Image, ImageList


class Api(object):
    def __init__(self, client_id=None, client_secret=None, access_token=None,
                 api_url=None, upload_url=None):
        """A Python interface for Gyazo API"""

        if api_url is None:
            self.api_url = 'https://api.gyazo.com'
        else:
            self.api_url = api_url

        if upload_url is None:
            self.upload_url = 'https://upload.gyazo.com'
        else:
            self.upload_url = upload_url

        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = access_token

    def get_image_list(self, page=1, per_page=20):
        """Return a list of user's saved images"""
        url = self.api_url + '/api/images'
        parameters = {}
        parameters['page'] = page
        parameters['per_page'] = per_page
        response = self._request_url(url, 'get', parameters)
        headers, result = self._parse_and_check(response)
        images = ImageList.from_list(result)
        images.set_from_headers(headers)
        return images

    def delete_image(self, image_id):
        """Delete an image"""
        url = self.api_url + '/api/images/' + image_id
        response = self._request_url(url, 'delete')
        headers, result = self._parse_and_check(response)
        print(result)

    def _request_url(self, url, method, data=None):
        headers = {'Authorization': 'Bearer ' + self._access_token}

        if method == 'get':
            try:
                return requests.get(url, data=data, headers=headers)
            except requests.RequestException as e:
                raise GyazoError(str(e))
        elif method == 'delete':
            try:
                return requests.delete(url, headers=headers)
            except requests.RequestException as e:
                raise GyazoError(str(e))

        # Unsupported method
        return None

    def _parse_and_check(self, data):
        data_dict = {}
        try:
            headers = data.headers
            data_dict = data.json()
        except Exception as e:
            raise e

        if data.status_code >= 400:
            message = data_dict.get('message', 'Error')
            raise GyazoError(message)

        return (headers, data_dict,)
