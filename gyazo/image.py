from __future__ import division
import json
import math

import dateutil.parser
import dateutil.tz
import requests

from .error import GyazoError


class Image(object):
    """A class representing an image of Gyazo"""

    def __init__(self, **kwargs):
        #: The time this image was created
        self.created_at = kwargs['created_at']
        #: An image ID
        self.image_id = kwargs.get('image_id')
        #: A permalink URL
        self.permalink_url = kwargs.get('permalink_url')
        #: A thumbnail URL
        self.thumb_url = kwargs['thumb_url']
        #: A type of the image
        self.type = kwargs['type']
        #: An image URL
        self.url = kwargs.get('url')

    @staticmethod
    def from_dict(data):
        """Create a new instance from dict

        :param data: A JSON dict
        """
        created_at = data.get('created_at', None)
        if created_at:
            created_at = dateutil.parser.parse(created_at)

        return Image(created_at=created_at,
                     image_id=data.get('image_id', None),
                     permalink_url=data.get('permalink_url', None),
                     thumb_url=data.get('thumb_url', None),
                     type=data.get('type', None),
                     url=data.get('url', None))

    def __str__(self):
        """Return a string representation of this instance"""
        return self.to_json()

    def __unicode__(self):
        """Return a string representation of this instance"""
        return self.to_json()

    def __or__(self, other):
        if not isinstance(other, Image):
            return NotImplemented

        attrs = (
            'created_at',
            'image_id',
            'permalink_url',
            'thumb_url',
            'type',
            'url'
        )

        kwargs = {}
        for attr in attrs:
            attr1 = getattr(self, attr, "")
            attr2 = getattr(other, attr, "")
            if attr1 != "":
                kwargs[attr] = attr1
            elif attr2 != "":
                kwargs[attr] = attr2

        return Image(**kwargs)

    @property
    def filename(self):
        """An image filename

        :getter: Return an image filename if it exists
        """
        if self.url:
            return self.url.split('/')[-1]
        return None

    @property
    def thumb_filename(self):
        """A thumbnail image filename

        :getter: Return a thumbnail filename
        """
        return self.thumb_url.split('/')[-1]

    @property
    def local_created_at(self):
        """The time this image was created in local time zone

        :getter: Return the time this image was created in local time zone
        """
        return self.created_at.astimezone(dateutil.tz.tzlocal())

    def to_json(self, indent=None, sort_keys=True):
        """Return a JSON string representation of this instance

        :param indent: specify an indent level or a string used to indent each
                       level
        :param sort_keys: the output is sorted by key
        """
        return json.dumps(self.to_dict(), indent=indent, sort_keys=sort_keys)

    def to_dict(self):
        """Return a dict representation of this instance"""
        data = {}

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

        return data

    def download(self):
        """Download an image file if it exists

        :raise GyazoError:
        """
        if self.url:
            try:
                return requests.get(self.url).content
            except requests.RequestException as e:
                raise GyazoError(str(e))
        return None

    def download_thumb(self):
        """Download a thumbnail image file

        :raise GyazoError:
        """
        try:
            return requests.get(self.thumb_url).content
        except requests.RequestException as e:
            raise GyazoError(str(e))


class ImageList(object):
    """A class representing a list of gyazo.Image"""

    def __init__(self, **kwargs):
        #: The number of images
        self.total_count = kwargs.get('total_count')
        #: Current page number
        self.current_page = kwargs.get('current_page')
        #: The number of images per page
        self.per_page = kwargs.get('per_page')
        #: User type
        self.user_type = kwargs.get('user_type')
        #: List of images
        self.images = kwargs.get('images', [])

    def __len__(self):
        return len(self.images)

    def __getitem__(self, key):
        return self.images[key]

    def __setitem__(self, key, value):
        self.images[key] = value

    def __delitem__(self, key):
        del self.images[key]

    def __iter__(self):
        return self.images.__iter__()

    def __add__(self, other):
        if isinstance(other, ImageList):
            images = self.images + other.images
            return ImageList(images=images, total_count=len(images))
        return NotImplemented

    @property
    def num_pages(self):
        """The number of pages

        :getter: Return the number of pages
        """
        return math.ceil(self.total_count / self.per_page)

    def has_next_page(self):
        """Whether there is a next page or not

        :getter: Return true if there is a next page
        """
        return self.current_page < math.ceil(self.total_count / self.per_page)

    def has_previous_page(self):
        """Whether there is a previous page or not

        :getter: Return true if there is a previous page
        """
        return 0 < self.current_page

    def set_attributes_from_headers(self, headers):
        """Set instance attributes with HTTP header

        :param headers: HTTP header
        """
        self.total_count = headers.get('x-total-count', None)
        self.current_page = headers.get('x-current-page', None)
        self.per_page = headers.get('x-per-page', None)
        self.user_type = headers.get('x-user-type', None)

        if self.total_count:
            self.total_count = int(self.total_count)
        if self.current_page:
            self.current_page = int(self.current_page)
        if self.per_page:
            self.per_page = int(self.per_page)

    def to_json(self, indent=None, sort_keys=True):
        """Return a JSON string representation of this instance

        :param indent: specify an indent level or a string used to indent each
                       level
        :param sort_keys: the output of dictionaries is sorted by key
        """
        return json.dumps([i.to_dict() for i in self.images],
                          indent=indent, sort_keys=sort_keys)

    @staticmethod
    def from_list(data):
        """Create a new instance from list

        :param data: A JSON list
        """
        return ImageList(images=[Image.from_dict(d) for d in data])
