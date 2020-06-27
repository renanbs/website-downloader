import argparse
from bs4 import BeautifulSoup

from website_downloader.services.dir import create_output_dir, open_saved_page
from website_downloader.services.html import download_page
from website_downloader.services.image import ImageService
from website_downloader.services.utils import is_url


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


def _obtain_url_from_user():
    return input('You can provide a URL to be used as out base path to '
                 'download the files from the website. (n /  url) -> ')


def run() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    if is_url(args.input):
        create_output_dir(args.output)
        page = download_page(args.url, args.output)
    else:
        page = open_saved_page(args.input)

    parsed_page = BeautifulSoup(page, 'html.parser')

    if not args.url:
        url = _obtain_url_from_user()
    else:
        url = args.url

    image_service = ImageService(args.output, parsed_page, url)
    image_service.download_images()


if __name__ == "__main__":
    run()
