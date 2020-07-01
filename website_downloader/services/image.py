from bs4 import BeautifulSoup

from website_downloader.services.dir import DirectoryService
from website_downloader.services.utils import is_fb_pixel

import requests


class ImageService:
    def __init__(self, dir_service: DirectoryService, page: BeautifulSoup, url: str = None):
        self.dir_service = dir_service
        self.page = page
        self.url = url

    def _extract_images_from_page(self):
        raw_imgs = self.page.find_all('img')
        images = []

        for raw in raw_imgs:
            if is_fb_pixel(raw.attrs['src']):
                continue

            if raw.attrs['src'] not in images:
                images.append(raw.attrs['src'])

        return images

    def _download_images(self, images):
        for img in images:
            joined_filepath, joined_url = self.dir_service.obtain_joined_paths(img, self.url)

            response = requests.get(joined_url)

            if response.status_code == 200:
                with open(joined_filepath, 'wb') as file:
                    file.write(response.content)
            else:
                print(f'Could not download file: {joined_url}')

    def download_images(self):
        images = self._extract_images_from_page()
        self.dir_service.create_directory_structure(images)
        self._download_images(images)
