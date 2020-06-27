import os

from website_downloader.services.exception import ValidationException


def create_output_dir(output):
    if os.path.isdir(output):
        raise ValidationException('output directory already exists')
    try:
        os.mkdir(output)
    except OSError as e:
        print(f'Creation of the directory {str(e.strerror)} failed')


def open_saved_page(file_path):
    if not os.path.exists(f'{file_path}/index.html'):
        raise ValidationException('File does not exist')

    with open(f'{file_path}/index.html', 'r') as fh:
        lines = fh.read()
    return lines
