import os
from unittest.mock import Mock, patch

import pytest
from bs4 import BeautifulSoup


def file_loader(filename, binary=False):
    """Loads data from file"""
    read_option = 'r'
    if binary:
        read_option = 'rb'

    with open(filename, read_option) as f:
        data = f.read()

    return data


@pytest.fixture
def index1():
    filename = os.path.join(os.path.dirname(__file__), 'resources', 'index1.html')
    return file_loader(filename)


@pytest.fixture
def page1(index1):
    return BeautifulSoup(index1, 'html.parser')


@pytest.fixture
def image_list_page_1():
    return ['mkt/images/image1.png', 'mkt/images/image2.png', 'mkt/images/image3.jpg']


@pytest.fixture
def image1():
    filename = os.path.join(os.path.dirname(__file__), 'resources', 'image1.png')
    return file_loader(filename, True)


@pytest.fixture
def image2():
    filename = os.path.join(os.path.dirname(__file__), 'resources', 'image2.png')
    return file_loader(filename, True)


@pytest.fixture
def image3():
    filename = os.path.join(os.path.dirname(__file__), 'resources', 'image3.jpg')
    return file_loader(filename, True)


def test_should_get_image_list(image_service, page1, image_list_page_1):
    image_service.page = page1
    image_service.dir_service.create_directory_structure = Mock()
    image_service._download_images = Mock()

    image_service.download_images()

    image_service.dir_service.create_directory_structure.assert_called_with(image_list_page_1)


def test_should_download_images(image_service, page1, image_list_page_1, requests_mock, image1, image2, image3):
    image_service._extract_images_from_page = Mock(return_value=image_list_page_1)

    image1_url = os.path.join(image_service.url, image_list_page_1[0])
    requests_mock.get(image1_url, status_code=200, content=image1)

    image2_url = os.path.join(image_service.url, image_list_page_1[1])
    requests_mock.get(image2_url, status_code=200, content=image2)

    image3_url = os.path.join(image_service.url, image_list_page_1[2])
    requests_mock.get(image3_url, status_code=200, content=image3)

    image_service.download_images()

    image_path = os.path.join(image_service.dir_service.output_dir, image_list_page_1[0])
    saved_image = file_loader(image_path, True)
    assert saved_image == image1

    image_path = os.path.join(image_service.dir_service.output_dir, image_list_page_1[1])
    saved_image = file_loader(image_path, True)
    assert saved_image == image2

    image_path = os.path.join(image_service.dir_service.output_dir, image_list_page_1[2])
    saved_image = file_loader(image_path, True)
    assert saved_image == image3


def test_should_not_download_some_images(image_service, page1, image_list_page_1, requests_mock, image2, image3):
    image_service._extract_images_from_page = Mock(return_value=image_list_page_1)

    image1_url = os.path.join(image_service.url, image_list_page_1[0])
    requests_mock.get(image1_url, status_code=400)

    image2_url = os.path.join(image_service.url, image_list_page_1[1])
    requests_mock.get(image2_url, status_code=200, content=image2)

    image3_url = os.path.join(image_service.url, image_list_page_1[2])
    requests_mock.get(image3_url, status_code=200, content=image3)

    with patch('website_downloader.services.image.print') as mocked_print:
        image_service.download_images()

    mocked_print.assert_called_with('Could not download file: http://my-url.com/mkt/images/image1.png')

    assert not os.path.exists(os.path.join(image_service.dir_service.output_dir, image_list_page_1[0]))

    assert file_loader(os.path.join(image_service.dir_service.output_dir, image_list_page_1[1]), True) == image2

    assert file_loader(os.path.join(image_service.dir_service.output_dir, image_list_page_1[2]), True) == image3
