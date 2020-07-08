from website_downloader.services.files import FilesService
from website_downloader.services.utils import is_google_tag_manager


class ScriptsService(FilesService):
    def extract_elements_from_page(self):
        raw_links = self.page.find_all('script')

        for raw in raw_links:
            src = raw.attrs.get('src')

            if not src:
                continue

            if src not in self.raw_elements:
                self.raw_elements.append(src)

    def filter_elements(self):
        return list(filter(lambda elem: not is_google_tag_manager(elem), self.raw_elements))
