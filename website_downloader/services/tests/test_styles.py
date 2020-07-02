import os
from unittest.mock import Mock, patch

import pytest

from website_downloader.services.dir import DirectoryService
from website_downloader.services.utils import file_loader


@pytest.fixture
def css_list_page_1():
    return ['mkt/css/font-awesome.min.css', 'mkt/css/my_css.css', '/mkt/css/another_css.css']


@pytest.fixture
def css_list_page_2():
    return ['https://xyz.com/app/Views/public/css/font-awesome.min.css',
            'https://xyz.com/app/Views/public/mkt/css/my_css.css',
            'https://xyz.com/app/Views/public/mkt/css/another_css.css']


@pytest.fixture
def style1():
    filename = os.path.join(os.path.dirname(__file__), 'resources', 'font-awesome.min.css')
    return file_loader(filename, True)


@pytest.fixture
def style2():
    filename = os.path.join(os.path.dirname(__file__), 'resources', 'my_css.css')
    return file_loader(filename, True)


@pytest.fixture
def style3():
    filename = os.path.join(os.path.dirname(__file__), 'resources', 'another_css.css')
    return file_loader(filename, True)


@pytest.mark.parametrize('page, style_list', (
                        (pytest.lazy_fixture('page1'), pytest.lazy_fixture('css_list_page_1')),
                        (pytest.lazy_fixture('page2'), pytest.lazy_fixture('css_list_page_2')),))
def test_should_get_styles_list(styles_service, page, style_list):
    styles_service.page = page
    styles_service.dir_service.create_directory_structure = Mock()
    styles_service._download_styles = Mock()

    styles_service.download_styles()

    styles_service.dir_service.create_directory_structure.assert_called_with(style_list)


@pytest.mark.parametrize('page, style_list', (
                        (pytest.lazy_fixture('page1'), pytest.lazy_fixture('css_list_page_1')),
                        (pytest.lazy_fixture('page2'), pytest.lazy_fixture('css_list_page_2')),))
def test_should_download_styles(styles_service, page, style_list, requests_mock, style1, style2, style3):
    styles_service._extract_styles_from_page = Mock(return_value=style_list)

    style_path_1, style1_url = styles_service.dir_service.obtain_joined_paths(style_list[0], styles_service.url)
    requests_mock.get(style1_url, status_code=200, content=style1)

    style_path_2, style2_url = styles_service.dir_service.obtain_joined_paths(style_list[1], styles_service.url)
    requests_mock.get(style2_url, status_code=200, content=style2)

    style_path_3, style3_url = styles_service.dir_service.obtain_joined_paths(style_list[2], styles_service.url)
    requests_mock.get(style3_url, status_code=200, content=style3)

    styles_service.download_styles()

    saved_style = file_loader(style_path_1, True)
    assert saved_style == style1

    saved_style = file_loader(style_path_2, True)
    assert saved_style == style2

    saved_style = file_loader(style_path_3, True)
    assert saved_style == style3


def test_should_not_download_some_styles(styles_service, page1, css_list_page_1, requests_mock, style2, style3):
    styles_service._extract_styles_from_page = Mock(return_value=css_list_page_1)

    style1_url = os.path.join(styles_service.url, css_list_page_1[0])
    requests_mock.get(style1_url, status_code=400)

    style2_url = os.path.join(styles_service.url, css_list_page_1[1])
    requests_mock.get(style2_url, status_code=200, content=style2)

    style3_url = os.path.join(styles_service.url, css_list_page_1[2])
    requests_mock.get(style3_url, status_code=200, content=style3)

    with patch('website_downloader.services.styles.print') as mocked_print:
        styles_service.download_styles()

    mocked_print.assert_called_with('Could not download file: http://my-url.com/mkt/css/font-awesome.min.css')

    assert not os.path.exists(os.path.join(styles_service.dir_service.output_dir, css_list_page_1[0]))

    assert file_loader(os.path.join(styles_service.dir_service.output_dir, css_list_page_1[1]), True) == style2

    assert file_loader(os.path.join(styles_service.dir_service.output_dir,
                                    DirectoryService.remove_root(css_list_page_1[2])), True) == style3
