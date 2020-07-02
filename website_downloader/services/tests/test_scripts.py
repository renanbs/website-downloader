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
def script1():
    filename = os.path.join(os.path.dirname(__file__), 'resources', 'font-awesome.min.css')
    return file_loader(filename, True)


@pytest.fixture
def script2():
    filename = os.path.join(os.path.dirname(__file__), 'resources', 'my_css.css')
    return file_loader(filename, True)


@pytest.fixture
def script3():
    filename = os.path.join(os.path.dirname(__file__), 'resources', 'another_css.css')
    return file_loader(filename, True)


@pytest.mark.parametrize('page, script_list', (
                        (pytest.lazy_fixture('page1'), pytest.lazy_fixture('css_list_page_1')),
                        (pytest.lazy_fixture('page2'), pytest.lazy_fixture('css_list_page_2')),))
def test_should_get_image_list(scripts_service, page, script_list):
    scripts_service.page = page
    scripts_service.dir_service.create_directory_structure = Mock()
    scripts_service._download_scripts = Mock()

    scripts_service.download_scripts()

    scripts_service.dir_service.create_directory_structure.assert_called_with(script_list)


@pytest.mark.parametrize('page, script_list', (
                        (pytest.lazy_fixture('page1'), pytest.lazy_fixture('css_list_page_1')),
                        (pytest.lazy_fixture('page2'), pytest.lazy_fixture('css_list_page_2')),))
def test_should_download_scripts(scripts_service, page, script_list, requests_mock, script1, script2, script3):
    scripts_service._extract_scripts_from_page = Mock(return_value=script_list)

    script_path_1, script1_url = scripts_service.dir_service.obtain_joined_paths(script_list[0], scripts_service.url)
    requests_mock.get(script1_url, status_code=200, content=script1)

    script_path_2, script2_url = scripts_service.dir_service.obtain_joined_paths(script_list[1], scripts_service.url)
    requests_mock.get(script2_url, status_code=200, content=script2)

    script_path_3, script3_url = scripts_service.dir_service.obtain_joined_paths(script_list[2], scripts_service.url)
    requests_mock.get(script3_url, status_code=200, content=script3)

    scripts_service.download_scripts()

    saved_script = file_loader(script_path_1, True)
    assert saved_script == script1

    saved_script = file_loader(script_path_2, True)
    assert saved_script == script2

    saved_script = file_loader(script_path_3, True)
    assert saved_script == script3


def test_should_not_download_some_scripts(scripts_service, page1, css_list_page_1, requests_mock, script2, script3):
    scripts_service._extract_scripts_from_page = Mock(return_value=css_list_page_1)

    script1_url = os.path.join(scripts_service.url, css_list_page_1[0])
    requests_mock.get(script1_url, status_code=400)

    script2_url = os.path.join(scripts_service.url, css_list_page_1[1])
    requests_mock.get(script2_url, status_code=200, content=script2)

    script3_url = os.path.join(scripts_service.url, css_list_page_1[2])
    requests_mock.get(script3_url, status_code=200, content=script3)

    with patch('website_downloader.services.scripts.print') as mocked_print:
        scripts_service.download_scripts()

    mocked_print.assert_called_with('Could not download file: http://my-url.com/mkt/css/font-awesome.min.css')

    assert not os.path.exists(os.path.join(scripts_service.dir_service.output_dir, css_list_page_1[0]))

    assert file_loader(os.path.join(scripts_service.dir_service.output_dir, css_list_page_1[1]), True) == script2

    assert file_loader(os.path.join(scripts_service.dir_service.output_dir,
                                    DirectoryService.remove_root(css_list_page_1[2])), True) == script3
