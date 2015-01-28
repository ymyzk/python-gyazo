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
    def __init__(self, **kwargs):
        self.created_at = kwargs.get('created_at', None)
        self.image_id = kwargs.get('image_id', None)
        self.permalink_url = kwargs.get('permalink_url', None)
        self.star = kwargs.get('star', None)
        self.thumb_url = kwargs.get('thumb_url', None)
        self.type = kwargs.get('type', None)
        self.url = kwargs.get('url', None)

    def __or__(self, other):
        if not isinstance(other, Image):
            raise NotImplemented

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

    @property
    def filename(self):
        if self.url:
            return self.url.split('/')[-1]
        return None

    @property
    def thumb_filename(self):
        if self.thumb_url:
            return self.thumb_url.split('/')[-1]
        return None

    @property
    def local_created_at(self):
        if self.created_at:
            return self.created_at.astimezone(dateutil.tz.tzlocal())
        return None

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def to_dict(self):
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
        if self.url:
            try:
                return requests.get(self.url).content
            except requests.RequestException as e:
                raise GyazoError(str(e))
        return None

    def download_thumb(self):
        if self.thumb_url:
            try:
                return requests.get(self.thumb_url).content
            except requests.RequestException as e:
                raise GyazoError(str(e))
        return None

    def __str__(self):
        return self.to_json()

    @staticmethod
    def from_dict(data):
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


class ImageList(object):
    def __init__(self, **kwargs):
        self.total_count = kwargs.get('total_count', None)
        self.current_page = kwargs.get('current_page', None)
        self.per_page = kwargs.get('per_page', None)
        self.user_type = kwargs.get('user_type', None)
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

    def __or__(self, other):
        if not isinstance(other, ImageList):
            raise NotImplemented

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

    @property
    def num_pages(self):
        return math.ceil(self.total_count / self.per_page)

    def has_next_page(self):
        return self.current_page < math.ceil(self.total_count / self.per_page)

    def has_previous_page(self):
        return 0 < self.current_page

    def set_attributes_from_headers(self, headers):
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

    @staticmethod
    def from_list(data):
        return ImageList(images=[Image.from_dict(d) for d in data])