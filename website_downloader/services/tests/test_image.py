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
def page1():
    file_loaded = file_loader(os.path.join(os.path.dirname(__file__), 'resources', 'index1.html'))
    return BeautifulSoup(file_loaded, 'html.parser')


@pytest.fixture
def page2():
    file_loaded = file_loader(os.path.join(os.path.dirname(__file__), 'resources', 'index2.html'))
    return BeautifulSoup(file_loaded, 'html.parser')


@pytest.fixture
def image_list_page_1():
    return ['/mkt/images/image1.png', 'mkt/images/image2.png', 'mkt/images/image3.jpg']


@pytest.fixture
def image_list_page_2():
    return ['https://xyz.com/app/Views/public/mkt/images/image1.png',
            'https://xyz.com/app/Views/public/mkt/images/image2.png',
            'https://xyz.com/app/Views/public/mkt/images/image3.jpg']


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


@pytest.mark.parametrize('page, image_list', (
                        (pytest.lazy_fixture('page1'), pytest.lazy_fixture('image_list_page_1')),
                        (pytest.lazy_fixture('page2'), pytest.lazy_fixture('image_list_page_2')),))
def test_should_get_image_list(image_service, page, image_list):
    image_service.page = page
    image_service.dir_service.create_directory_structure = Mock()
    image_service._download_images = Mock()

    image_service.download_images()

    image_service.dir_service.create_directory_structure.assert_called_with(image_list)


@pytest.mark.parametrize('page, image_list', (
                        (pytest.lazy_fixture('page1'), pytest.lazy_fixture('image_list_page_1')),
                        (pytest.lazy_fixture('page2'), pytest.lazy_fixture('image_list_page_2')),))
def test_should_download_images(image_service, page, image_list, requests_mock, image1, image2, image3):
    image_service._extract_images_from_page = Mock(return_value=image_list)

    image_path_1, image1_url = image_service.dir_service.obtain_joined_paths(image_list[0], image_service.url)
    requests_mock.get(image1_url, status_code=200, content=image1)

    image_path_2, image2_url = image_service.dir_service.obtain_joined_paths(image_list[1], image_service.url)
    requests_mock.get(image2_url, status_code=200, content=image2)

    image_path_3, image3_url = image_service.dir_service.obtain_joined_paths(image_list[2], image_service.url)
    requests_mock.get(image3_url, status_code=200, content=image3)

    image_service.download_images()

    saved_image = file_loader(image_path_1, True)
    assert saved_image == image1

    saved_image = file_loader(image_path_2, True)
    assert saved_image == image2

    saved_image = file_loader(image_path_3, True)
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
