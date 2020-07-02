from website_downloader.services.files import FilesService
from website_downloader.services.utils import is_google_tag_manager


class ScriptsService(FilesService):
    def extract_from_page(self):
        raw_links = self.page.find_all('script')
        scripts = []

        for raw in raw_links:
            src = raw.attrs.get('src')

            if not src or is_google_tag_manager(src):
                continue

            if src not in scripts:
                scripts.append(src)

        return scripts
