import os
from urllib import parse
from pathlib import Path

from website_downloader.services.exception import ValidationException
from website_downloader.services.utils import fix_url


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
    def create_directory_structure(files):
        for item in files.items():
            dirname = os.path.dirname(item[0])

            if not os.path.exists(dirname):
                path = Path(dirname)
                path.mkdir(parents=True, exist_ok=True)

    def obtain_joined_paths(self, item_url):
        item_url = fix_url(item_url)
        filepath = os.path.join(self.output_dir, self.remove_root(parse.urlsplit(item_url).path))

        url = parse.urlsplit(item_url).geturl()
        if not url.startswith('http'):
            filepath = os.path.join(self.output_dir, self.remove_root(url))

        return filepath
