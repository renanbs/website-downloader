import requests

from website_downloader.services.exception import ValidationException


def download_page(url, output):
    response = requests.get(url)

    if response.status_code == 200:
        with open(f'{output}/index.html', 'w') as file:
            file.write(response.text)
        return response.text
    else:
        raise ValidationException(f'Could not download main site from {url}')
