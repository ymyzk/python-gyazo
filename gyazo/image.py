from datetime import datetime
import json
import math
from typing import (Any, Dict, Iterable, Iterator, List, Mapping,
                    Optional, Union)

import dateutil.parser
import dateutil.tz
import requests

from .error import GyazoError


class Image:
    """A class representing an image of Gyazo"""

    def __init__(self, **kwargs: Any) -> None:
        #: The time this image was created
        self.created_at = kwargs['created_at']  # type: datetime
        #: An image ID
        self.image_id = kwargs.get('image_id')  # type: Optional[str]
        #: A permalink URL
        self.permalink_url = kwargs.get('permalink_url')  # type: Optional[str]
        #: A thumbnail URL
        self.thumb_url = kwargs.get('thumb_url')  # type: Optional[str]
        #: A type of the image
        self.type = kwargs['type']  # type: str
        #: An image URL
        self.url = kwargs.get('url')  # type: Optional[str]
        #: Result of OCR
        self.ocr = kwargs.get('ocr')  # type: Optional[Dict[str, str]]

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> 'Image':
        """Create a new instance from dict

        :param data: A JSON dict
        """
        kwargs = {}
        for k, v in data.items():
            if isinstance(v, str) and v == '':
                continue
            elif isinstance(v, list) and v == []:
                continue
            elif isinstance(v, dict) and v == {}:
                continue
            elif k == 'created_at' and v:
                kwargs[k] = dateutil.parser.parse(v)
            else:
                kwargs[k] = v

        return Image(**kwargs)

    def __str__(self) -> str:
        """Return a string representation of this instance"""
        return self.to_json()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Image):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __or__(self, other: 'Image') -> 'Image':
        if not isinstance(other, Image):
            return NotImplemented

        attrs = (
            'created_at',
            'image_id',
            'permalink_url',
            'thumb_url',
            'type',
            'url',
        )

        kwargs = {}
        for attr in attrs:
            attr1 = getattr(self, attr, "")
            attr2 = getattr(other, attr, "")
            if attr1 is not None and attr1 != "":
                kwargs[attr] = attr1
            elif attr2 is not None and attr2 != "":
                kwargs[attr] = attr2
        if self.ocr is not None or other.ocr is not None:
            kwargs["ocr"] = {**(other.ocr or {}), **(self.ocr or {})}

        return Image(**kwargs)

    @property
    def filename(self) -> Optional[str]:
        """An image filename

        :getter: Return an image filename if it exists
        """
        if self.url is None or self.url == '':
            return None
        return self.url.split('/')[-1]

    @property
    def thumb_filename(self) -> Optional[str]:
        """A thumbnail image filename

        :getter: Return a thumbnail filename
        """
        if self.thumb_url is None or self.thumb_url == '':
            return None
        return self.thumb_url.split('/')[-1]

    @property
    def local_created_at(self) -> datetime:
        """The time this image was created in local time zone

        :getter: Return the time this image was created in local time zone
        """
        return self.created_at.astimezone(dateutil.tz.tzlocal())

    def to_json(self,
                indent: Optional[Union[int, str]] = None,
                sort_keys: bool = True) -> str:
        """Return a JSON string representation of this instance

        :param indent: specify an indent level or a string used to indent each
                       level
        :param sort_keys: the output is sorted by key
        """
        return json.dumps(self.to_dict(), indent=indent, sort_keys=sort_keys)

    def to_dict(self) -> Dict[str, Any]:
        """Return a dict representation of this instance"""
        data = {}  # type: Dict[str, Any]

        if self.created_at:
            data['created_at'] = self.created_at.strftime(
                '%Y-%m-%dT%H:%M:%S%z')
        if self.image_id:
            data['image_id'] = self.image_id
        if self.permalink_url:
            data['permalink_url'] = self.permalink_url
        if self.thumb_url:
            data['thumb_url'] = self.thumb_url
        if self.type:
            data['type'] = self.type
        if self.url:
            data['url'] = self.url
        if self.ocr:
            data['ocr'] = self.ocr

        return data

    def download(self) -> Optional[bytes]:
        """Download an image file if it exists

        :raise GyazoError:
        """
        if self.url is None or self.url == '':
            return None
        try:
            return requests.get(self.url).content
        except requests.RequestException as e:
            raise GyazoError(str(e))

    def download_thumb(self) -> Optional[bytes]:
        """Download a thumbnail image file

        :raise GyazoError:
        """
        if self.thumb_url is None or self.thumb_url == '':
            return None
        try:
            return requests.get(self.thumb_url).content
        except requests.RequestException as e:
            raise GyazoError(str(e))


class ImageList:
    """A class representing a list of gyazo.Image"""

    def __init__(self, **kwargs: Any) -> None:
        #: The number of images
        self.total_count = kwargs.get('total_count')  # type: Optional[int]
        #: Current page number (1-index)
        self.current_page = kwargs.get('current_page')  # type: Optional[int]
        #: The number of images per page
        self.per_page = kwargs.get('per_page')  # type: Optional[int]
        #: User type
        self.user_type = kwargs.get('user_type')  # type: Optional[str]
        #: List of images
        self.images = kwargs.get('images', [])  # type: List[Image]

    def __len__(self) -> int:
        return len(self.images)

    def __getitem__(self, key: int) -> Image:
        return self.images[key]

    def __setitem__(self, key: int, value: Image) -> None:
        self.images[key] = value

    def __delitem__(self, key: int) -> None:
        del self.images[key]

    def __iter__(self) -> Iterator[Image]:
        return self.images.__iter__()

    def __add__(self, other: 'ImageList') -> 'ImageList':
        if isinstance(other, ImageList):
            images = self.images + other.images
            return ImageList(images=images, total_count=len(images))
        return NotImplemented

    @property
    def num_pages(self) -> Optional[int]:
        """The number of pages

        :getter: Return the number of pages
        """
        if self.total_count is not None and self.per_page is not None:
            return math.ceil(self.total_count / self.per_page)
        else:
            return None

    @property
    def has_next_page(self) -> Optional[bool]:
        """Whether there is a next page or not

        :getter: Return true if there is a next page
        """
        if (
                self.current_page is not None
                and self.total_count is not None
                and self.per_page is not None
        ):
            num_pages = math.ceil(self.total_count / self.per_page)
            return 0 < self.current_page < num_pages
        else:
            return None

    @property
    def has_previous_page(self) -> Optional[bool]:
        """Whether there is a previous page or not

        :getter: Return true if there is a previous page
        """
        if self.current_page is not None:
            return 1 < self.current_page
        else:
            return None

    def set_attributes_from_headers(self, headers: Mapping[str, str]) -> None:
        """Set instance attributes with HTTP header

        :param headers: HTTP header
        """
        total_count = headers.get('x-total-count', None)
        current_page = headers.get('x-current-page', None)
        per_page = headers.get('x-per-page', None)
        self.user_type = headers.get('x-user-type', None)

        if total_count:
            self.total_count = int(str(total_count))
        if current_page:
            self.current_page = int(str(current_page))
        if per_page:
            self.per_page = int(str(per_page))

    def to_json(self,
                indent: Optional[Union[int, str]] = None,
                sort_keys: bool = True) -> str:
        """Return a JSON string representation of this instance

        :param indent: specify an indent level or a string used to indent each
                       level
        :param sort_keys: the output of dictionaries is sorted by key
        """
        return json.dumps([i.to_dict() for i in self.images],
                          indent=indent, sort_keys=sort_keys)

    @staticmethod
    def from_list(data: Iterable[Mapping[str, Any]]) -> 'ImageList':
        """Create a new instance from list

        :param data: A JSON list
        """
        return ImageList(images=[Image.from_dict(d) for d in data])
