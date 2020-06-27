from unittest.mock import MagicMock

import pytest

from website_downloader.services.image import ImageService


@pytest.fixture
def source_url():
    return 'http://my-url.com'


@pytest.fixture
def image_service(tmpdir, source_url):
    return ImageService(str(tmpdir), MagicMock(), source_url)
