import os
from unittest.mock import mock_open, patch

import pytest

from website_downloader.services.exception import ValidationException
from website_downloader.services.html import download_page


def test_should_download_index_html(requests_mock, tmp_path):
    url = 'http://xyz.com'
    content = 'just the content'
    requests_mock.get(url, status_code=200, text=content)

    with patch('website_downloader.services.html.open', mock_open()) as mocked_file:
        result = download_page(url, tmp_path)

        mocked_file.assert_called_once_with(os.path.join(str(tmp_path.absolute()), 'index.html'), 'w')

        mocked_file().write.assert_called_once_with(content)
        assert content == result


def test_should_not_download_index_html(requests_mock, tmp_path):
    url = 'http://xyz.com'
    requests_mock.get(url, status_code=409)

    with patch('website_downloader.services.html.open', mock_open()) as mocked_file:
        with pytest.raises(ValidationException) as e:
            download_page(url, tmp_path)

        assert str(e.value) == f'Could not download main site from {url}'
        mocked_file.assert_not_called()
        mocked_file().write.assert_not_called()
