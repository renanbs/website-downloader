from bs4 import BeautifulSoup

from website_downloader.services.utils import is_fb_pixel

import os
from urllib import parse
import requests
from pathlib import Path


class ImageService:
    def __init__(self, output_dir: str, page: BeautifulSoup, url: str = None):
        self.output_dir = output_dir
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

    def _create_images_directory(self, images):
        for img in images:
            joined_dir = os.path.join(self.output_dir, os.path.dirname(img))

            if not os.path.exists(joined_dir):
                path = Path(joined_dir)
                path.mkdir(parents=True, exist_ok=True)

    def _download_images(self, images):
        for img in images:
            joined_filepath = os.path.join(self.output_dir, img)

            if not img.startswith('/'):
                joined_url = os.path.join(self.url, img)
            else:
                joined_url = parse.urljoin(self.url, img)

            response = requests.get(joined_url)

            if response.status_code == 200:
                with open(joined_filepath, 'wb') as file:
                    file.write(response.content)
            else:
                print(f'Could not download file: {joined_url}')

    def download_images(self):
        images = self._extract_images_from_page()
        self._create_images_directory(images)
        self._download_images(images)
