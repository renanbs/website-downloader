import argparse
import os
from urllib import parse
import requests
from pathlib import Path
from bs4 import BeautifulSoup

from website_downloader.utils import is_fb_pixel, is_url


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='wb_downloader',
                                     usage='%(prog)s [OPTIONS]...',
                                     description='Downloads the given website.')

    parser.add_argument('-v', '--version', action='version', version=f'{parser.prog} version 1.0.0')

    parser.add_argument('-i', '--input', action='store', type=str, required=True,
                        help='website to download, or input file to process.')
    parser.add_argument('-u', '--url', action='store', type=str, required=False,
                        help='base url to be used with the input.')

    parser.add_argument('-o', '--output', action='store', type=str, required=False,
                        help='where your are going to save your files.')
    return parser


class ValidationException(Exception):
    pass


def _create_output_dir(output):
    if os.path.isdir(output):
        raise ValidationException('output directory already exists')
    try:
        os.mkdir(output)
    except OSError as e:
        print(f'Creation of the directory {str(e.strerror)} failed')


def download_page(url, output):
    response = requests.get(url)
    with open(f'{output}/index.html', 'w') as file:
        file.write(response.text)
    return response.text


def _open_saved_page(file_path):
    if not os.path.exists(f'{file_path}/index.html'):
        raise ValidationException('File does not exist')

    with open(f'{file_path}/index.html', 'r') as fh:
        lines = fh.read()
    return lines


def _extract_images_to_download(page):
    raw_imgs = page.find_all('img')
    images = []

    for raw in raw_imgs:
        if is_fb_pixel(raw.attrs['src']):
            continue

        if raw.attrs['src'] not in images:
            images.append(raw.attrs['src'])

    return images


def _obtain_url_from_user():
    return input('You can provide a URL to be used as out base path to '
                 'download the files from the website. (n /  url) -> ')


def _prepare_images_directory(images, output):
    for img in images:
        joined_dir = os.path.join(output, os.path.dirname(img))

        if not os.path.exists(joined_dir):
            path = Path(joined_dir)
            path.mkdir(parents=True, exist_ok=True)


def _download_images(images, output, url):
    for img in images:

        joined_filepath = os.path.join(output, img)
        if not img.startswith('/'):
            joined_url = os.path.join(url, img)
        else:
            joined_url = parse.urljoin(url, img)
        response = requests.get(joined_url)

        if response.status_code == 200:
            with open(joined_filepath, 'wb') as file:
                file.write(response.content)
        else:
            print(f'Could not download file: {joined_url}')


def run() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    if is_url(args.input):
        _create_output_dir(args.output)
        page = download_page(args.url, args.output)
    else:
        page = _open_saved_page(args.input)

    soup = BeautifulSoup(page, 'html.parser')

    if not args.url:
        url = _obtain_url_from_user()
    else:
        url = args.url

    images = _extract_images_to_download(soup)
    _prepare_images_directory(images, args.output)
    _download_images(images, args.output, url=url)


if __name__ == "__main__":
    run()
