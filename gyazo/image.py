#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import json

import dateutil.parser


class Image(object):
    def __init__(self, **kwargs):
        defaults = {
            'created_at': None,
            'image_id': None,
            'permalink_url': None,
            'star': None,
            'thumb_url': None,
            'type': None,
            'url': None
        }
        for key in defaults:
            setattr(self, key, kwargs.get(key, defaults[key]))

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
        defaults = {
            'total_count': None,
            'current_page': None,
            'per_page': None,
            'user_type': None,
            'images': []
        }
        for key in defaults:
            setattr(self, key, kwargs.get(key, defaults[key]))

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

    def set_from_headers(self, headers):
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
