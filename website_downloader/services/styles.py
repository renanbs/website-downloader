from website_downloader.services.files import FilesService
from website_downloader.services.utils import is_google_font, is_favicon


class StylesService(FilesService):
    def extract_elements_from_page(self):
        raw_links = self.page.find_all('link')

        for raw in raw_links:
            # TODO: remove this if
            if raw.attrs.get('rel') and 'canonical' in raw.attrs.get('rel')[0]:
                continue

            if not raw.attrs.get('href'):
                continue

            url = raw.attrs['href']

            if url not in self.raw_elements:
                self.raw_elements.append(url)

    def filter_elements(self):
        first_filter = list(filter(lambda elem: not is_google_font(elem), self.raw_elements))
        self.elements = list(filter(lambda elem: not is_favicon(elem), first_filter))
