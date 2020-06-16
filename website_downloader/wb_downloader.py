import argparse
import os
from urllib import parse
import requests
from bs4 import BeautifulSoup


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='wb_downloader',
                                     usage='%(prog)s [OPTIONS] [OUTPUT]...',
                                     description='Downloads the given website.')

    parser.add_argument('-v', '--version', action='version', version=f'{parser.prog} version 1.0.0')

    parser.add_argument('-i', '--input', action='store', type=str, required=True,
                        help='website to download, or input file to process.')
    # parser.add_argument('url', type=str, help='website to download')
    parser.add_argument('output', type=str, help='output of the website downloaded')
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


def download_and_save_page(url, output):
    response = requests.get(url)
    with open(f'{output}/index.html', 'w') as file:
        file.write(response.text)
    return response.text


def _is_fb_pixel(image):
    if 'PageView' in image:
        return True
    return False


def _open_saved_page(file_path):
    if not os.path.exists(f'{file_path}/index.html'):
        raise ValidationException('File does not exist')

    with open(f'{file_path}/index.html', 'r') as fh:
        lines = fh.read()
    return lines


def _extract_images_to_download(page, url=None):
    raw_imgs = page.find_all('img')
    images = []
    for raw in raw_imgs:
        if _is_fb_pixel(raw.attrs['src']):
            continue

        joined_url = raw.attrs['src']
        if url:
            joined_url = parse.urljoin(url, raw.attrs['src'])

        if joined_url not in images:
            images.append(joined_url)

    return images


def run() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    # _create_output_dir(args.output)
    # page = download_and_save_page(args.url, args.output)
    page = _open_saved_page(args.output)
    soup = BeautifulSoup(page, 'html.parser')
    print(_extract_images_to_download(soup))


if __name__ == "__main__":
    run()
