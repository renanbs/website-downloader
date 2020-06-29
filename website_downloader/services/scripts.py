import os
from urllib import parse

import requests
from bs4 import BeautifulSoup

from website_downloader.services.dir import DirectoryService
from website_downloader.services.utils import is_google_font, is_favicon


class ScriptService:
    def __init__(self, dir_service: DirectoryService, page: BeautifulSoup, url: str = None):
        self.dir_service = dir_service
        self.page = page
        self.url = url

    def _extract_scripts_from_page(self):
        raw_links = self.page.find_all('link')
        scripts = []

        for raw in raw_links:
            if is_google_font(raw.attrs['href']) or is_favicon(raw.attrs['href']):
                continue

            if raw.attrs['href'] not in scripts:
                scripts.append(raw.attrs['href'])

        return scripts

    def _download_scripts(self, scripts):
        for script in scripts:
            joined_url = parse.urlsplit(script).geturl()
            if not joined_url.startswith('http'):
                joined_filepath = os.path.join(self.dir_service.output_dir, script)
                if not script.startswith('/'):
                    joined_url = os.path.join(self.url, script)
                else:
                    joined_url = parse.urljoin(self.url, script)
            else:
                filepath = self.dir_service.remove_root(parse.urlsplit(script).path)
                joined_filepath = os.path.join(self.dir_service.output_dir, filepath)

            response = requests.get(joined_url)

            if response.status_code == 200:
                with open(joined_filepath, 'wb') as file:
                    file.write(response.content)
            else:
                print(f'Could not download file: {joined_url}')

    def download_scripts(self):
        scripts = self._extract_scripts_from_page()
        self.dir_service.create_directory_structure(scripts)
        self._download_scripts(scripts)
