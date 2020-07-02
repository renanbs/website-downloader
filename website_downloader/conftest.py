from unittest.mock import MagicMock

import pytest

from website_downloader.services.dir import DirectoryService
from website_downloader.services.images import ImagesService
from website_downloader.services.styles import StyleService


@pytest.fixture
def source_url():
    return 'http://my-url.com'


@pytest.fixture
def dir_service(tmpdir):
    return DirectoryService(str(tmpdir))


@pytest.fixture
def image_service(dir_service, source_url):
    return ImagesService(dir_service, MagicMock(), source_url)


@pytest.fixture
def styles_service(dir_service, source_url):
    return StyleService(dir_service, MagicMock(), source_url)
