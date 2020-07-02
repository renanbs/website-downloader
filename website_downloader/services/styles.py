from website_downloader.services.files import FilesService
from website_downloader.services.utils import is_google_font, is_favicon


class StyleService(FilesService):
    def extract_from_page(self):
        raw_links = self.page.find_all('link')
        styles = []

        for raw in raw_links:
            if is_google_font(raw.attrs['href']) or is_favicon(raw.attrs['href']):
                continue

            if raw.attrs['href'] not in styles:
                styles.append(raw.attrs['href'])

        return styles
