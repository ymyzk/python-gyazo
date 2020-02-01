from datetime import datetime, timedelta, timezone

import pytest

from gyazo.image import Image, ImageList


image_1_dict = {
    'url': 'https://i.gyazo.com/2c9044330d710fca3da64b222eddf5b5.png',
    'type': 'png',
    'created_at': '2014-07-25T08:29:51+0000',
    'image_id': '2c9044330d710fca3da64b222eddf5b5',
    'thumb_url': 'https://i.gyazo.com/thumb/180/_242799a7d541869e0b73dc93ee113fb5.png',
    'permalink_url': 'http://gyazo.com/2c9044330d710fca3da64b222eddf5b5',
}
image_1 = Image(
    url='https://i.gyazo.com/2c9044330d710fca3da64b222eddf5b5.png',
    type='png',
    created_at=datetime(2014, 7, 25, 8, 29, 51, tzinfo=timezone.utc),
    image_id='2c9044330d710fca3da64b222eddf5b5',
    thumb_url='https://i.gyazo.com/thumb/180/_242799a7d541869e0b73dc93ee113fb5.png',
    permalink_url='http://gyazo.com/2c9044330d710fca3da64b222eddf5b5',
)
image_2_dict = {
    'type': 'png',
    'created_at': '2014-06-21T13:45:46+0900',
    'thumb_url': 'https://thumb.gyazo.com/thumb/200/Qa1W1MKHxBhbk-png.jpg',
}
image_2 = Image(
    type='png',
    created_at=datetime(2014, 6, 21, 13, 45, 46, tzinfo=timezone(timedelta(hours=9))),
    thumb_url='https://thumb.gyazo.com/thumb/200/Qa1W1MKHxBhbk-png.jpg',
)
image_2_dict_empty_str = {
    'url': '',
    'type': 'png',
    'created_at': '2014-06-21T13:45:46+0900',
    'image_id': '',
    'thumb_url': 'https://thumb.gyazo.com/thumb/200/Qa1W1MKHxBhbk-png.jpg',
    'permalink_url': ''
}
image_2_empty_str = Image(
    url='',
    type='png',
    created_at=datetime(2014, 6, 21, 13, 45, 46, tzinfo=timezone(timedelta(hours=9))),
    image_id='',
    thumb_url='https://thumb.gyazo.com/thumb/200/Qa1W1MKHxBhbk-png.jpg',
    permalink_url='',
)
image_3_partial = Image(
    url='',
    type='png',
    created_at=datetime(2014, 7, 20, 3, 9, 34, tzinfo=timezone.utc),
    image_id='',
    thumb_url='https://i.gyazo.com/thumb/180/_eadaaad52408b1e53c09111d6959139f.png',
    permalink_url='',
)
image_3 = Image(
    url='https://i.gyazo.com/9d04d2da1b4daaaa234c68b5219dc1e3.png',
    type='png',
    created_at=datetime(2014, 7, 20, 3, 9, 34, tzinfo=timezone.utc),
    image_id='9d04d2da1b4daaaa234c68b5219dc1e3',
    thumb_url='https://i.gyazo.com/thumb/180/_eadaaad52408b1e53c09111d6959139f.png',
    permalink_url='http://gyazo.com/9d04d2da1b4daaaa234c68b5219dc1e3'
)

test_data_from_dict = [
    (image_1_dict, image_1),
    (image_2_dict, image_2),
    (image_2_dict_empty_str, image_2),
]

test_data_to_dict = [
    (image_1, image_1_dict),
    (image_2, image_2_dict),
    (image_2_empty_str, image_2_dict),
]

test_data_to_json = [
    (
        image_1,
        '{"created_at": "2014-07-25T08:29:51+0000", '
        '"image_id": "2c9044330d710fca3da64b222eddf5b5", '
        '"permalink_url": "http://gyazo.com/2c9044330d710fca3da64b222eddf5b5", '
        '"thumb_url": "https://i.gyazo.com/thumb/180/'
        '_242799a7d541869e0b73dc93ee113fb5.png", "type": "png", '
        '"url": "https://i.gyazo.com/2c9044330d710fca3da64b222eddf5b5.png"}'
    ),
]

test_data_filenames = [
    (
        image_1,
        '2c9044330d710fca3da64b222eddf5b5.png',
        '_242799a7d541869e0b73dc93ee113fb5.png',
    ),
    (
        image_2,
        None,
        'Qa1W1MKHxBhbk-png.jpg',
    ),
    (
        image_2_empty_str,
        None,
        'Qa1W1MKHxBhbk-png.jpg',
    ),
]


class TestImage:
    @pytest.mark.parametrize("d,image", test_data_from_dict)
    def test_from_dict(self, d, image):
        assert Image.from_dict(d) == image

    @pytest.mark.parametrize("image,filename,thumb_filename", test_data_filenames)
    def test_filenames(self, image, filename, thumb_filename):
        assert image.filename == filename
        assert image.thumb_filename == thumb_filename

    @pytest.mark.parametrize("image,expected", test_data_to_dict)
    def test_to_dict(self, image, expected):
        assert image.to_dict() == expected

    @pytest.mark.parametrize("image,expected", test_data_to_json)
    def test_to_json(self, image, expected):
        assert image.to_json() == expected

    def test_or(self):
        assert image_3_partial | image_3 == image_3


class TestImageList:
    def test_from_list(self):
        l = ImageList.from_list([image_1_dict, image_2_dict, image_2_dict_empty_str])
        assert l.images == [image_1, image_2, image_2]

    @pytest.mark.parametrize("image_list,expected", [
        (ImageList(total_count=23, per_page=10, current_page=0), False),
        (ImageList(total_count=23, per_page=10, current_page=3), False),
        (ImageList(total_count=20, per_page=10, current_page=1), True),
        (ImageList(total_count=20, per_page=10), None),
        (ImageList(total_count=20, current_page=3), None),
        (ImageList(per_page=10, current_page=3), None),
    ])
    def test_has_next_page(self, image_list, expected):
        assert image_list.has_next_page == expected

    @pytest.mark.parametrize("image_list,expected", [
        (ImageList(current_page=2), True),
        (ImageList(current_page=1), False),
        (ImageList(), None),
    ])
    def test_has_previous_page(self, image_list, expected):
        assert image_list.has_previous_page == expected

    def test_add(self):
        l1 = ImageList(images=[image_1, image_2])
        l2 = ImageList(images=[image_3])
        l = l1 + l2
        assert l.total_count == 3
        assert len(l.images) == 3
        assert l.current_page is None
        assert l.per_page is None
        assert l.user_type is None

    def test_set_attributes_from_headers(self):
        headers = {
            'server': 'nginx/1.11.9',
            'date': 'Sat, 01 Feb 2020 16:43:58 GMT',
            'content-type': 'application/json; charset=utf-8',
            'x-total-count': '1144',
            'x-current-page': '1',
            'x-per-page': '20',
            'x-user-type': 'ninja',
        }
        il = ImageList()
        il.set_attributes_from_headers(headers)
        assert il.total_count == 1144
        assert il.current_page == 1
        assert il.per_page == 20
        assert il.user_type == 'ninja'