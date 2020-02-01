from typing import Any, BinaryIO, Dict, MutableMapping, Optional, Tuple

import requests
from requests.models import Response

from .error import GyazoError
from .image import Image, ImageList


class Api:
    """A Python interface for Gyazo API"""

    def __init__(self,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 access_token: Optional[str] = None,
                 api_url: str = 'https://api.gyazo.com',
                 upload_url: str = 'https://upload.gyazo.com') -> None:
        """
        :param client_id: (optional) API client ID
        :param client_secret: (optional) API secret
        :param access_token: (optional) API access token
        :param api_url: (optional) API endpoint URL
                        (default: https://api.gyazo.com)
        :param upload_url: (optional) Upload API endpoint URL
                           (default: https://upload.gyazo.com)
        """
        self.api_url = api_url  # type: str
        self.upload_url = upload_url  # type: str
        self._client_id = client_id  # type: Optional[str]
        self._client_secret = client_secret  # type: Optional[str]
        self._access_token = access_token  # type: Optional[str]

    def get_image_list(self, page: int = 1, per_page: int = 20) -> ImageList:
        """Return a list of user's saved images

        :param page: (optional) Page number (default: 1)
        :param per_page: (optional) Number of images per page
                         (default: 20, min: 1, max: 100)
        """
        url = self.api_url + '/api/images'
        params = {
            'page': page,
            'per_page': per_page
        }
        response = self._request_url(
            url, 'get', params=params, with_access_token=True)
        headers, result = self._parse_and_check(response)
        images = ImageList.from_list(result)
        images.set_attributes_from_headers(headers)
        return images

    def get_image(self, image_id: str) -> Image:
        """Get an image

        :param image_id: Image ID
        """
        url = self.api_url + '/api/images/' + image_id
        response = self._request_url(url, 'get', with_access_token=True)
        headers, result = self._parse_and_check(response)
        return Image.from_dict(result)

    def upload_image(self,
                     image_file: BinaryIO,
                     referer_url: Optional[str] = None,
                     title: Optional[str] = None,
                     desc: Optional[str] = None,

                     created_at: Optional[float] = None,
                     collection_id: Optional[str] = None) -> Image:
        """Upload an image

        :param image_file: File-like object of an image file
        :param referer_url: Referer site URL
        :param title: Site title
        :param desc: Comment
        :param created_at: Image's created time in unix time
        :param collection_id: Collection ID
        """
        url = self.upload_url + '/api/upload'
        data = {}
        if referer_url is not None:
            data['referer_url'] = referer_url
        if title is not None:
            data['title'] = title
        if desc is not None:
            data['desc'] = desc
        if created_at is not None:
            data['created_at'] = str(created_at)
        if collection_id is not None:
            data['collection_id'] = collection_id
        files = {
            'imagedata': image_file
        }
        response = self._request_url(
            url, 'post', data=data, files=files, with_access_token=True)
        headers, result = self._parse_and_check(response)
        return Image.from_dict(result)

    def delete_image(self, image_id: str) -> Image:
        """Delete an image

        :param image_id: Image ID
        """
        url = self.api_url + '/api/images/' + image_id
        response = self._request_url(url, 'delete', with_access_token=True)
        headers, result = self._parse_and_check(response)
        return Image.from_dict(result)

    def get_oembed(self, url: str) -> Dict[str, Any]:
        """Return an oEmbed format json dictionary

        :param url: Image page URL (ex. http://gyazo.com/xxxxx)
        """
        api_url = self.api_url + '/api/oembed'
        parameters = {
            'url': url
        }
        response = self._request_url(api_url, 'get', params=parameters)
        _, result = (
            self._parse_and_check(response)
        )  # type: Tuple[Any, Dict[str, Any]]
        return result

    def _request_url(self,
                     url: str,
                     method: str,
                     params: Optional[Dict[str, Any]] = None,
                     data: Optional[Dict[str, Any]] = None,
                     files: Optional[Dict[str, BinaryIO]] = None,
                     with_client_id: bool = False,
                     with_access_token: bool = False) -> Response:
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
        if params is None:
            params = {}

        if with_client_id and self._client_id is not None:
            params['client_id'] = self._client_id

        if with_access_token and self._access_token is not None:
            headers['Authorization'] = "Bearer " + self._access_token

        try:
            return requests.request(method, url,
                                    params=params,
                                    data=data,
                                    files=files,
                                    headers=headers)
        except requests.RequestException as e:
            raise GyazoError(str(e))

    def _parse_and_check(
            self,
            data: Response
    ) -> Tuple[MutableMapping[str, str], Any]:
        try:
            headers = data.headers
            json_data = data.json()
        except Exception as e:
            raise e

        if data.status_code >= 400:
            message = json_data.get('message', 'Error')
            raise GyazoError(message)

        return headers, json_data
