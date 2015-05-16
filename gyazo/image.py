#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals
import json
import math

import dateutil.parser
import dateutil.tz
import requests

from .error import GyazoError


class Image(object):
    """A class representing an image of Gyazo"""

    def __init__(self, **kwargs):
        #: The time this image was created (datetime)
        self.created_at = kwargs.get('created_at', None)
        #: An image ID (str or unicode)
        self.image_id = kwargs.get('image_id', None)
        #: A permalink URL (str of unicode)
        self.permalink_url = kwargs.get('permalink_url', None)
        #: An image is stared or not (bool)
        self.star = kwargs.get('star', None)
        #: A thumbnail URL
        self.thumb_url = kwargs.get('thumb_url', None)
        #: A type of the image
        self.type = kwargs.get('type', None)
        #: An image URL
        self.url = kwargs.get('url', None)

    @staticmethod
    def from_dict(data):
        """Create a new instance from dict

        :param data: A JSON dict
        :type data: dict
        :rtype: Image
        """
        created_at = data.get('created_at', None)
        if created_at:
            created_at = dateutil.parser.parse(created_at)

        return Image(created_at=created_at,
                     image_id=data.get('image_id', None),
                     permalink_url=data.get('permalink_url', None),
                     star=data.get('star', None),
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
        if isinstance(other, Image):
            attrs = (
                'created_at',
                'image_id',
                'permalink_url',
                'star',
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
        return NotImplemented

    @property
    def filename(self):
        """An image filename

        :getter: Return an image filename if it exists
        :rtype: str | unicode
        """
        if self.url:
            return self.url.split('/')[-1]
        return None

    @property
    def thumb_filename(self):
        """A thumbnail image filename

        :getter: Return a thumbnail filename if it exists
        :rtype: str | unicode
        """
        if self.thumb_url:
            return self.thumb_url.split('/')[-1]
        return None

    @property
    def local_created_at(self):
        """The time this image was created in local time zone

        :getter: Return the time this image was created in local time zone
                 if it exists
        """
        if self.created_at:
            return self.created_at.astimezone(dateutil.tz.tzlocal())
        return None

    def to_json(self, indent=None, sort_keys=True):
        """Return a JSON string representation of this instance

        :param indent: specify an indent level or a string used to indent each
                       level
        :type indent: int | str
        :param sort_keys: the output is sorted by key
        :type sort_keys: bool
        :rtype: str | unicode
        """
        return json.dumps(self.to_dict(), indent=indent, sort_keys=sort_keys)

    def to_dict(self):
        """Return a dict representation of this instance

        :rtype: dict
        """
        data = {}

        if self.created_at:
            data['created_at'] = self.created_at.strftime(
                '%Y-%m-%dT%H:%M:%S%z')
        if self.image_id:
            data['image_id'] = self.image_id
        if self.permalink_url:
            data['permalink_url'] = self.permalink_url
        if self.star:
            data['star'] = self.star
        if self.thumb_url:
            data['thumb_url'] = self.thumb_url
        if self.type:
            data['type'] = self.type
        if self.url:
            data['url'] = self.url

        return data

    def download(self):
        """Download an image file

        :rtype: bytes | str
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

        :rtype: bytes | str
        :raise GyazoError:
        """
        if self.thumb_url:
            try:
                return requests.get(self.thumb_url).content
            except requests.RequestException as e:
                raise GyazoError(str(e))
        return None


class ImageList(object):
    """A class representing a list of gyazo.Image"""

    def __init__(self, **kwargs):
        #: The number of images (int)
        self.total_count = kwargs.get('total_count', None)
        #: Current page number (int)
        self.current_page = kwargs.get('current_page', None)
        #: The number of images per page (int)
        self.per_page = kwargs.get('per_page', None)
        #: User type (str or unicode)
        self.user_type = kwargs.get('user_type', None)
        #: List of images (list of gyazo.Image)
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

    def __or__(self, other):
        if isinstance(other, ImageList):
            index_1 = {}
            for image in self:
                index_1[image.thumb_url] = image

            index_2 = {}
            for image in other:
                index_2[image.thumb_url] = image

            for key in index_2:
                if key in index_1:
                    index_1[key] |= index_2[key]
                else:
                    index_1[key] = index_2[key]

            images = index_1.values()
            return ImageList(images=sorted(images,
                                           key=lambda i: i.created_at,
                                           reverse=True),
                             total_count=len(images))

        return NotImplemented

    @property
    def num_pages(self):
        """The number of pages

        :getter: Return the number of pages
        :rtype: int
        """
        return math.ceil(self.total_count / self.per_page)

    def has_next_page(self):
        """Whether there is a next page or not

        :getter: Return true if there is a next page
        :rtype: bool
        """
        return self.current_page < math.ceil(self.total_count / self.per_page)

    def has_previous_page(self):
        """Whether there is a previous page or not

        :getter: Return true if there is a previous page
        :rtype: bool
        """
        return 0 < self.current_page

    def set_attributes_from_headers(self, headers):
        """Set instance attributes with HTTP header

        :param headers: HTTP header
        :type headers: dict
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
        :type indent: int | str
        :param sort_keys: the output of dictionaries is sorted by key
        :type sort_keys: bool
        :rtype: str | unicode
        """
        return json.dumps([i.to_dict() for i in self.images],
                          indent=indent, sort_keys=sort_keys)

    @staticmethod
    def from_list(data):
        """Create a new instance from list

        :param data: A JSON list
        :type data: list
        :rtype: ImageList
        """
        return ImageList(images=[Image.from_dict(d) for d in data])
