import argparse
import os
from urllib import parse
import requests
from bs4 import BeautifulSoup


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS] [URL] [OUTPUT]...",
        description="Downloads the given website.",
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )

    parser.add_argument('url', type=str, help='website to download')
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


def _extract_images_to_download(page, url):
    raw_imgs = page.find_all('img')
    images = []
    for raw in raw_imgs:
        if _is_fb_pixel(raw.attrs['src']):
            continue

        joined_url = parse.urljoin(url, raw.attrs['src'])

        if joined_url not in images:
            images.append(joined_url)

    return images


def run() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    _create_output_dir(args.output)
    page = download_and_save_page(args.url, args.output)
    soup = BeautifulSoup(page, 'html.parser')
    _extract_images_to_download(soup, args.url)



if __name__ == "__main__":
    run()
