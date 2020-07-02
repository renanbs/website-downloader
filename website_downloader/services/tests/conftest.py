import os

import pytest
from bs4 import BeautifulSoup

from website_downloader.services.utils import file_loader


@pytest.fixture
def page1():
    file_loaded = file_loader(os.path.join(os.path.dirname(__file__), 'resources', 'index1.html'))
    return BeautifulSoup(file_loaded, 'html.parser')


@pytest.fixture
def page2():
    file_loaded = file_loader(os.path.join(os.path.dirname(__file__), 'resources', 'index2.html'))
    return BeautifulSoup(file_loaded, 'html.parser')
