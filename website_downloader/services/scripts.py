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

    def download_scripts(self):
        scripts = self._extract_scripts_from_page()
        self.dir_service.create_directory_structure(scripts)
