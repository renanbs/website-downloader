from website_downloader.services.files import FilesService
from website_downloader.services.utils import is_google_font, is_favicon


class StylesService(FilesService):
    def extract_from_page(self):
        raw_links = self.page.find_all('link')
        styles = []

        for raw in raw_links:
            url = self.obtain_download_url(raw.attrs['href'])
            if is_google_font(url) or is_favicon(url):
                continue

            if url not in styles:
                styles.append(url)

        return styles
