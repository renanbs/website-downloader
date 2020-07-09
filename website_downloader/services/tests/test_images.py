from unittest.mock import MagicMock

import pytest


@pytest.fixture
def filtered_image_list():
    return ['/mkt/images/image1.png', '/mkt/images/image-from-data-src.png',
            'https://xyz.com/app/Views/public/mkt/images/image2.png', 'mkt/images/image2.png', 'mkt/images/image3.jpg']


@pytest.fixture
def unfiltered_image_list():
    return ['https://www.facebook.com/tr?id=18885911215512&ev=PageView&noscript=1', '/mkt/images/image1.png',
            '/mkt/images/image-from-data-src.png', 'https://xyz.com/app/Views/public/mkt/images/image2.png',
            'mkt/images/image2.png', 'mkt/images/image3.jpg']


def test_should_get_filtered_image_list(image_service, page1, filtered_image_list, unfiltered_image_list):
    image_service.page = page1
    image_service.dir_service.create_directory_structure = MagicMock()
    image_service._download = MagicMock()

    image_service.download()

    assert image_service.elements == filtered_image_list
    assert image_service.raw_elements == unfiltered_image_list
