import requests
from bs4 import BeautifulSoup

from website_downloader.services.dir import DirectoryService
from website_downloader.services.utils import is_google_font, is_favicon


class StyleService:
    def __init__(self, dir_service: DirectoryService, page: BeautifulSoup, url: str = None):
        self.dir_service = dir_service
        self.page = page
        self.url = url

    def _extract_styles_from_page(self):
        raw_links = self.page.find_all('link')
        styles = []

        for raw in raw_links:
            if is_google_font(raw.attrs['href']) or is_favicon(raw.attrs['href']):
                continue

            if raw.attrs['href'] not in styles:
                styles.append(raw.attrs['href'])

        return styles

    def _extract_scripts_from_page(self):
        raw_links = self.page.find_all('script')
        scripts = []

        for raw in raw_links:
            if is_google_font(raw.attrs['href']) or is_favicon(raw.attrs['href']):
                continue

            if raw.attrs['href'] not in scripts:
                scripts.append(raw.attrs['href'])

        return scripts

    def _download_styles(self, styles):
        for style in styles:
            joined_filepath, joined_url = self.dir_service.obtain_joined_paths(style, self.url)

            response = requests.get(joined_url)

            if response.status_code == 200:
                with open(joined_filepath, 'wb') as file:
                    file.write(response.content)
            else:
                print(f'Could not download file: {joined_url}')

    def download_styles(self):
        styles = self._extract_styles_from_page()
        self.dir_service.create_directory_structure(styles)
        self._download_styles(styles)
