from website_downloader.services.files import FilesService
from website_downloader.services.utils import is_fb_pixel


class ImagesService(FilesService):
    def extract_elements_from_page(self):
        raw_imgs = self.page.find_all('img')

        for raw in raw_imgs:
            if not raw.attrs.get('src') and not raw.attrs.get('data-src'):
                continue

            if raw.attrs.get('data-src') and raw.attrs['data-src'] not in self.raw_elements:
                self.raw_elements.append(raw.attrs['data-src'])
                continue

            if raw.attrs.get('src') and raw.attrs['src'] not in self.raw_elements:
                self.raw_elements.append(raw.attrs['src'])
                continue

    def filter_elements(self):
        self.elements = list(filter(lambda elem: not is_fb_pixel(elem), self.raw_elements))
