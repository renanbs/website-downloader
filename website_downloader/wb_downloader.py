import argparse
from bs4 import BeautifulSoup

from website_downloader.services.dir import open_saved_page, DirectoryService
from website_downloader.services.html import download_page
from website_downloader.services.images import ImagesService
from website_downloader.services.scripts import ScriptsService
from website_downloader.services.styles import StylesService
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


def run() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    dir_service = DirectoryService(args.output)

    if is_url(args.input):
        dir_service.create_output_dir()
        page = download_page(args.input, args.output)
    else:
        page = open_saved_page(args.input)

    parsed_page = BeautifulSoup(page, 'html.parser')

    url = args.url
    if not args.url:
        url = args.input

    scripts_service = ScriptsService(dir_service, parsed_page, url)
    scripts_service.download()

    styles_service = StylesService(dir_service, parsed_page, url)
    styles_service.download()

    image_service = ImagesService(dir_service, parsed_page, url)
    image_service.download()


if __name__ == "__main__":
    run()
