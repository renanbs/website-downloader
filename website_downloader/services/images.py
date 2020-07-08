from website_downloader.services.files import FilesService
from website_downloader.services.utils import is_fb_pixel


class ImagesService(FilesService):
    def extract_elements_from_page(self):
        raw_imgs = self.page.find_all('img')
        images = []

        for raw in raw_imgs:
            if is_fb_pixel(raw.attrs['src']):
                continue

            if raw.attrs['src'] not in images:
                images.append(raw.attrs['src'])

        return images
