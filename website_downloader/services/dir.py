import os
from urllib import parse
from pathlib import Path

from website_downloader.services.exception import ValidationException


def open_saved_page(file_path):
    if not os.path.exists(f'{file_path}/index.html'):
        raise ValidationException('File does not exist')

    with open(f'{file_path}/index.html', 'r') as fh:
        lines = fh.read()
    return lines


class DirectoryService:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def create_output_dir(self):
        if os.path.isdir(self.output_dir):
            raise ValidationException('output directory already exists')
        try:
            os.mkdir(self.output_dir)
        except OSError as e:
            print(f'Creation of the directory {str(e.strerror)} failed')

    @staticmethod
    def remove_root(dirname):
        if dirname.startswith('/'):
            return dirname[1:len(dirname)]
        return dirname

    @staticmethod
    def fix_url(url):
        # TODO: Find a better place to put this method
        if url.startswith('http:///'):
            return url.replace('http:///', 'http://')
        if url.startswith('https:///'):
            return url.replace('https:///', 'https://')
        return url

    @staticmethod
    def create_directory_structure(files):
        # TODO: return the path created to use in the download method
        for item in files.items():
            # TODO: Do this line above only once
            # item = self.fix_url(item)
            # dirname = os.path.dirname(parse.urlsplit(item).path)
            # dirname = self.remove_root(dirname)
            #
            # joined_dir = os.path.join(self.output_dir, dirname)

            if not os.path.exists(item):
                path = Path(item)
                path.mkdir(parents=True, exist_ok=True)

    def obtain_joined_paths(self, item_url):
        item_url = self.fix_url(item_url)
        filepath = os.path.join(self.output_dir, self.remove_root(parse.urlsplit(item_url).path))

        url = parse.urlsplit(item_url).geturl()
        if not url.startswith('http'):
            filepath = os.path.join(self.output_dir, self.remove_root(url))

        return filepath
