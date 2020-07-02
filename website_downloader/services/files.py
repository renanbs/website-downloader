from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from website_downloader.services.dir import DirectoryService


class FilesService(ABC):
    def __init__(self, dir_service: DirectoryService, page: BeautifulSoup, url: str = None):
        self.dir_service = dir_service
        self.page = page
        self.url = url

    @abstractmethod
    def extract_from_page(self):
        pass

    def _download(self, files):
        for the_file in files:
            joined_filepath, joined_url = self.dir_service.obtain_joined_paths(the_file, self.url)

            response = requests.get(joined_url)

            if response.status_code == 200:
                with open(joined_filepath, 'wb') as file:
                    file.write(response.content)
            else:
                print(f'Could not download file: {joined_url}')

    def download(self):
        files = self.extract_from_page()
        self.dir_service.create_directory_structure(files)
        self._download(files)
