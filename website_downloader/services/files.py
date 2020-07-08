import os
from abc import ABC, abstractmethod
from urllib import parse

import requests
from bs4 import BeautifulSoup

from website_downloader.services.dir import DirectoryService


class FilesService(ABC):
    def __init__(self, dir_service: DirectoryService, page: BeautifulSoup, url: str = None):
        self.dir_service = dir_service
        self.page = page
        self.url = url
        self.raw_elements = []

    @abstractmethod
    def extract_elements_from_page(self):
        pass

    @abstractmethod
    def filter_elements(self):
        pass

    def obtain_download_url(self, the_file):
        url = parse.urlsplit(the_file).geturl()

        if url.startswith('http'):
            return self.dir_service.fix_url(url)

        if the_file.startswith('//'):
            return parse.urljoin(f'{parse.urlsplit(self.url).scheme}:', the_file[2:len(the_file)])

        return self.dir_service.remove_root(the_file)

    def obtain_output_path(self, the_file):
        pass

    def _obtain_download_url(self, item):
        url = parse.urlsplit(item).geturl()

        joined_url = self.dir_service.fix_url(url)

        if not url.startswith('http'):
            joined_url = os.path.join(self.url, url)

        return joined_url

    def _download(self, files):
        for the_file in files:
            joined_filepath = self.dir_service.obtain_joined_paths(self.dir_service.remove_root(the_file))

            joined_url = self._obtain_download_url(the_file)
            response = requests.get(joined_url,
                                    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                           'Chrome/80.0.3987.163 Safari/537.36'})

            if response.status_code == 200:
                with open(joined_filepath, 'wb') as file:
                    file.write(response.content)
            else:
                print(f'Could not download file: {joined_url}')

    def download(self):
        self.extract_elements_from_page()
        filtered = self.filter_elements()
        self.dir_service.create_directory_structure(filtered)
        self._download(filtered)
