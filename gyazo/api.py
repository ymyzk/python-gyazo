#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import requests
import six
from typing import Any, AnyStr, BinaryIO, Dict, Optional  # noqa: F401

from .error import GyazoError
from .image import Image, ImageList


class Api(object):
    """A Python interface for Gyazo API"""

    def __init__(self,
                 client_id=None,  # type: AnyStr
                 client_secret=None,  # type: AnyStr
                 access_token=None,  # type: AnyStr
                 api_url='https://api.gyazo.com',  # type: AnyStr
                 upload_url='https://upload.gyazo.com'  # type: AnyStr
                 ):
        # type: (...) -> None
        """
        :param client_id: API client ID
        :param client_secret: API secret
        :param access_token: API access token
        :param api_url: (optional) API endpoint URL
                        (default: https://api.gyazo.com)
        :param upload_url: (optional) Upload API endpoint URL
                           (default: https://upload.gyazo.com)
        """
        self.api_url = api_url
        self.upload_url = upload_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = access_token

    def get_image_list(self, page=1, per_page=20):
        # type: (int, int) -> ImageList
        """Return a list of user's saved images

        :param page: (optional) Page number (default: 1)
        :param per_page: (optional) Number of images per page
                         (default: 20, min: 1, max: 100)
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

    def upload_image(self,
                     image_file,  # type: BinaryIO
                     referer_url=None,  # type: AnyStr
                     title=None,  # type: AnyStr
                     desc=None,  # type: AnyStr
                     created_at=None,  # type: float
                     collection_id=None,  # type: AnyStr
                     ):
        # type: (...) -> Image
        """Upload an image

        :param image_file: File-like object of an image file
        :param referer_url: Referer site URL
        :param title: Site title
        :param desc: Comment
        :param created_at: Image's created time in unix time
        :param collection_id: Collection ID
        """
        url = self.upload_url + '/api/upload'
        parameters = {}
        if referer_url is not None:
            parameters['referer_url'] = referer_url
        if title is not None:
            parameters['title'] = title
        if desc is not None:
            parameters['desc'] = desc
        if created_at is not None:
            parameters['created_at'] = created_at
        if collection_id is not None:
            parameters['collection_id'] = collection_id
        files = {
            'imagedata': image_file
        }
        response = self._request_url(
            url, 'post', data=parameters, files=files, with_access_token=True)
        headers, result = self._parse_and_check(response)
        return Image.from_dict(result)

    def delete_image(self, image_id):
        # type: (AnyStr) -> Image
        """Delete an image

        :param image_id: Image ID
        """
        url = self.api_url + '/api/images/' + image_id
        response = self._request_url(url, 'delete', with_access_token=True)
        headers, result = self._parse_and_check(response)
        return Image.from_dict(result)

    def get_oembed(self, url):
        # type: (AnyStr) -> Dict[str, Any]
        """Return an oEmbed format json dictionary

        :param url: Image page URL (ex. http://gyazo.com/xxxxx)
        """
        api_url = self.api_url + '/api/oembed'
        parameters = {
            'url': url
        }
        response = self._request_url(api_url, 'get', parameters)
        headers, result = self._parse_and_check(response)
        return result

    def _request_url(self,
                     url,  # type: AnyStr
                     method,  # type: AnyStr
                     data=None,  # type: Dict[str, Any]
                     files=None,  # type: Dict[str, BinaryIO]
                     with_client_id=False,  # type: bool
                     with_access_token=False  # type: bool
                     ):
        # type: (...) -> Optional[requests.models.Response]
        """Send HTTP request

        :param url: URL
        :param method: HTTP method (get, post or delete)
        :param with_client_id: send request with client_id (default: false)
        :param with_access_token: send request with with_access_token
                                  (default: false)
        :raise GyazoError:
        """
        headers = {}  # type: Dict[str, Any]
        if data is None:
            data = {}

        if with_client_id and self._client_id is not None:
            data['client_id'] = self._client_id

        if with_access_token and self._access_token is not None:
            data['access_token'] = self._access_token

        if method == 'get':
            try:
                return requests.get(url, params=data, headers=headers)
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
                return requests.delete(url, params=data, headers=headers)
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
