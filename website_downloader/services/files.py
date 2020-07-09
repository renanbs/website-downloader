import os
from abc import ABC, abstractmethod
from urllib import parse

import requests
from bs4 import BeautifulSoup

from website_downloader.services.dir import DirectoryService
from website_downloader.services.utils import fix_url


class FilesService(ABC):
    def __init__(self, dir_service: DirectoryService, page: BeautifulSoup, url: str = None):
        self.dir_service = dir_service
        self.page = page
        self.url = url
        self.raw_elements = []
        self.elements = []

    @abstractmethod
    def extract_elements_from_page(self):
        pass

    @abstractmethod
    def filter_elements(self):
        pass

    def _obtain_download_url(self, the_file):
        url = parse.urlsplit(the_file).geturl()

        if url.startswith('http'):
            return fix_url(url)

        if the_file.startswith('//'):
            return parse.urljoin(f'{parse.urlsplit(self.url).scheme}:', the_file[2:len(the_file)])

        return os.path.join(parse.urlsplit(self.url).geturl(), self.dir_service.remove_root(url))

    def _obtain_output_path(self, the_file):
        return os.path.join(self.dir_service.output_dir,
                            self.dir_service.remove_root(parse.urlsplit(the_file).path))

    def obtain_download_and_output_path(self):
        output_file = []
        files_with_download_url = dict()

        for elem in self.elements:
            url = self._obtain_download_url(elem)
            output = self._obtain_output_path(elem)
            output_file.append(output)
            files_with_download_url[output] = url

        return files_with_download_url, output_file

    @staticmethod
    def _download(files):
        for the_file in files.items():
            response = requests.get(the_file[1],
                                    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                           'Chrome/80.0.3987.163 Safari/537.36'})

            if response.status_code == 200:
                with open(the_file[0], 'wb') as file:
                    file.write(response.content)
            else:
                print(f'Could not download file: {the_file[1]}')

    def download(self):
        self.extract_elements_from_page()
        self.filter_elements()

        files_with_download_url, output_file = self.obtain_download_and_output_path()

        self.dir_service.create_directory_structure(files_with_download_url)
        self._download(files_with_download_url)
