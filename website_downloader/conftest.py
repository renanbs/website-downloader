from unittest.mock import MagicMock

import pytest

from website_downloader.services.dir import DirectoryService
from website_downloader.services.image import ImageService
from website_downloader.services.scripts import ScriptService


@pytest.fixture
def source_url():
    return 'http://my-url.com'


@pytest.fixture
def dir_service(tmpdir):
    return DirectoryService(str(tmpdir))


@pytest.fixture
def image_service(dir_service, source_url):
    return ImageService(dir_service, MagicMock(), source_url)


@pytest.fixture
def scripts_service(dir_service, source_url):
    return ScriptService(dir_service, MagicMock(), source_url)
