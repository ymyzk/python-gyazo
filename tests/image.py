#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
import unittest

import dateutil.parser

from gyazo import Image, ImageList


class TestImage(unittest.TestCase):
    def setUp(self):
        self.samples = [
            {
                'url': 'https://i.gyazo.com/2c9044330d710fca3da64b222eddf5b5.png',
                'type': 'png',
                'created_at': '2014-07-25T08:29:51+0000',
                'image_id': '2c9044330d710fca3da64b222eddf5b5',
                'thumb_url': 'https://i.gyazo.com/thumb/180/_242799a7d541869e0b73dc93ee113fb5.png',
                'permalink_url': 'http://gyazo.com/2c9044330d710fca3da64b222eddf5b5'},
            {
                'url': 'https://i.gyazo.com/9d04d2da1b4daaaa234c68b5219dc1e3.png',
                'type': 'png',
                'created_at': '2014-07-20T03:09:34+0900',
                'image_id': '9d04d2da1b4daaaa234c68b5219dc1e3',
                'thumb_url': 'https://i.gyazo.com/thumb/180/_eadaaad52408b1e53c09111d6959139f.png',
                'permalink_url': 'http://gyazo.com/9d04d2da1b4daaaa234c68b5219dc1e3'},
            {
                'url': '',
                'type': 'png',
                'created_at': '2014-06-21T13:45:46+0000',
                'image_id': '',
                'thumb_url': 'https://i.gyazo.com/thumb/180/_ebb000813faac4c0572cc0fc0b2d8ede.png',
                'permalink_url': ''
            }
        ]
        self.filenames = [
            '2c9044330d710fca3da64b222eddf5b5.png',
            '9d04d2da1b4daaaa234c68b5219dc1e3.png',
            None
        ]
        self.thumbnames = [
            '_242799a7d541869e0b73dc93ee113fb5.png',
            '_eadaaad52408b1e53c09111d6959139f.png',
            '_ebb000813faac4c0572cc0fc0b2d8ede.png'
        ]

    def test_from_dict(self):
        for sample in self.samples:
            image = Image.from_dict(sample)
            self.assertIsNotNone(image)

    def test_to_dict(self):
        for sample in self.samples:
            image = Image.from_dict(sample).to_dict()
            for key in sample:
                if sample[key] is not None and sample[key] != '':
                    self.assertEqual(sample[key], image[key])

    def test_filename(self):
        for sample, filename in zip(self.samples, self.filenames):
            image = Image.from_dict(sample)
            self.assertEqual(image.filename, filename)

    def test_thumb_filename(self):
        for sample, thumbname in zip(self.samples, self.thumbnames):
            image = Image.from_dict(sample)
            self.assertEqual(image.thumb_filename, thumbname)

    def test_or(self):
        dict_1 = {
            'url': '',
            'type': 'png',
            'created_at': '2014-07-20T03:09:34+0900',
            'image_id': '',
            'thumb_url': 'https://i.gyazo.com/thumb/180/_eadaaad52408b1e53c09111d6959139f.png',
            'permalink_url': ''
        }
        dict_2 = {
            'url': 'https://i.gyazo.com/9d04d2da1b4daaaa234c68b5219dc1e3.png',
            'type': 'png',
            'created_at': '2014-07-20T03:09:34+0900',
            'image_id': '9d04d2da1b4daaaa234c68b5219dc1e3',
            'thumb_url': 'https://i.gyazo.com/thumb/180/_eadaaad52408b1e53c09111d6959139f.png',
            'permalink_url': 'http://gyazo.com/9d04d2da1b4daaaa234c68b5219dc1e3'
        }
        image_1 = Image.from_dict(dict_1)
        image_2 = Image.from_dict(dict_2)
        for image in (image_1 | image_2, image_2 | image_1):
            self.assertEqual(image.url, dict_2['url'])
            self.assertEqual(image.type, dict_2['type'])
            self.assertEqual(image.created_at,
                             dateutil.parser.parse(dict_2['created_at']))
            self.assertEqual(image.image_id, dict_2['image_id'])
            self.assertEqual(image.thumb_url, dict_2['thumb_url'])
            self.assertEqual(image.permalink_url, dict_2['permalink_url'])


class TestImageList(unittest.TestCase):
    def setUp(self):
        images_1_dict = [
            {
                'url': 'https://i.gyazo.com/2c9044330d710fca3da64b222eddf5b5.png',
                'type': 'png',
                'created_at': '2014-07-25T08:29:51+0000',
                'image_id': '2c9044330d710fca3da64b222eddf5b5',
                'thumb_url': 'https://i.gyazo.com/thumb/180/_242799a7d541869e0b73dc93ee113fb5.png',
                'permalink_url': 'http://gyazo.com/2c9044330d710fca3da64b222eddf5b5'
            },
            {
                'url': 'https://i.gyazo.com/9d04d2da1b4daaaa234c68b5219dc1e3.png',
                'type': 'png',
                'created_at': '2014-07-20T03:09:34+0900',
                'image_id': '9d04d2da1b4daaaa234c68b5219dc1e3',
                'thumb_url': 'https://i.gyazo.com/thumb/180/_eadaaad52408b1e53c09111d6959139f.png',
                'permalink_url': 'http://gyazo.com/9d04d2da1b4daaaa234c68b5219dc1e3'
            },
            {
                'url': '',
                'type': 'png',
                'created_at': '2014-06-21T13:45:46+0000',
                'image_id': '',
                'thumb_url': 'https://i.gyazo.com/thumb/180/_ebb000813faac4c0572cc0fc0b2d8ede.png',
                'permalink_url': ''
            }
        ]
        self.images = ImageList(
            images=[Image.from_dict(d) for d in images_1_dict])

    def test_has_next_page(self):
        il = ImageList()
        il.total_count = 23
        il.per_page = 10
        il.current_page = 0
        self.assertTrue(il.has_next_page())
        il.current_page = 3
        self.assertFalse(il.has_next_page())
        il.total_count = 20
        il.current_page = 0
        self.assertTrue(il.has_next_page())
        il.current_page = 2
        self.assertFalse(il.has_next_page())
        il.current_page = 4
        self.assertFalse(il.has_next_page())

    def test_has_previous_page(self):
        il = ImageList()
        il.current_page = 0
        self.assertFalse(il.has_previous_page())
        il.current_page = 1
        self.assertTrue(il.has_previous_page())

    def test_or(self):
        image_dict = {
            'url': 'https://i.gyazo.com/7654d2da1b4daaaa234c68b5219dc1e3.png',
            'type': 'png',
            'created_at': '2014-06-21T13:45:46+0000',
            'image_id': '7654d2da1b4daaaa234c68b5219dc1e3',
            'thumb_url': 'https://i.gyazo.com/thumb/180/_ebb000813faac4c0572cc0fc0b2d8ede.png',
            'permalink_url': 'http://gyazo.com/7654d2da1b4daaaa234c68b5219dc1e3'
        }
        images_2 = ImageList(images=[Image.from_dict(image_dict)])
        images_1 = self.images | images_2
        image = None
        for image in images_1:
            if image.thumb_url == image_dict['thumb_url']:
                break
        self.assertIsNotNone(image)
        self.assertEqual(image.url, image_dict['url'])
        self.assertEqual(image.type, image_dict['type'])
        self.assertEqual(image.created_at,
                         dateutil.parser.parse(image_dict['created_at']))
        self.assertEqual(image.image_id, image_dict['image_id'])
        self.assertEqual(image.thumb_url, image_dict['thumb_url'])
        self.assertEqual(image.permalink_url, image_dict['permalink_url'])
