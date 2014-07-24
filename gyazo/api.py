#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import requests

from .image import Image, ImageList


class Api(object):
    def __init__(self, client_id=None, client_secret=None, access_token=None,
                 api_url=None, upload_url=None):
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

    def get_list(self, page=1, per_page=20):
        url = self.api_url + '/api/images'
        parameters = {}
        parameters['page'] = page
        parameters['per_page'] = per_page
        response = self._request_url(url, 'get', parameters)
        headers, result = self._parse_and_check(response)
        images = ImageList.from_list(result)
        images.set_from_headers(headers)
        return images

    def _request_url(self, url, method, data=None):
        headers = {'Authorization': 'Bearer ' + self._access_token}
        if method == 'get':
            try:
                return requests.get(url, data=data, headers=headers)
            except:
                raise Exception()

        # Unsupported method
        return None

    def _parse_and_check(self, data):
        try:
            headers = data.headers
            data = data.json()
        except:
            raise Exception()

        return (headers, data,)
