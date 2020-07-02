from unittest.mock import Mock

import pytest


@pytest.fixture
def scripts_list_page_1():
    return ['https://xyz.com/app/Views/public/js/jquery.js',
            'https://xyz.com/app/Views/public/js/constants.js',
            'https://xyz.com/app/Views/public/mkt/js/slick.min.js',
            '/mkt/js/another-jquery2.js',
            'mkt/js/another-jquery.js',
            'mkt/js/another-slick.min.js']


def test_should_get_scripts_list(scripts_service, page1, scripts_list_page_1):
    scripts_service.page = page1
    scripts_service.dir_service.create_directory_structure = Mock()
    scripts_service._download = Mock()

    scripts_service.download()

    scripts_service.dir_service.create_directory_structure.assert_called_with(scripts_list_page_1)
