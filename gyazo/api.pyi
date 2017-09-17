from typing import Any, BinaryIO, Dict, MutableMapping, Optional, Tuple

from requests.models import Response

from .image import Image, ImageList


class Api:
    api_url: str
    upload_url: str
    _client_id: str
    _client_secret: str
    _access_token: str

    def __init__(self,
                 client_id: Optional[str] = ...,
                 client_secret: Optional[str] = ...,
                 access_token: Optional[str] = ...,
                 api_url: str = ...,
                 upload_url: str = ...) -> None: ...
    def get_image_list(self, page: int = ..., per_page: int = ...) -> ImageList: ...
    def upload_image(self,
                     image_file: BinaryIO,
                     referer_url: Optional[str] = ...,
                     title: Optional[str] = ...,
                     desc: Optional[str] = ...,
                     created_at: Optional[float] = ...,
                     collection_id: Optional[str] = ...) -> Image: ...
    def delete_image(self, image_id: str) -> Image: ...
    def get_oembed(self, url: str) -> Dict[str, Any]: ...

    # Private
    def _request_url(self,
                     url: str,
                     method: str,
                     params: Optional[Dict[str, Any]] = ...,
                     data: Optional[Dict[str, Any]] = ...,
                     files: Optional[Dict[str, BinaryIO]] = ...,
                     with_client_id: bool = ...,
                     with_access_token: bool = ...) -> Response: ...
    def _parse_and_check(self, data: Response) -> Tuple[MutableMapping[str, str], Any]: ...
