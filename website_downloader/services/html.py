import requests

from website_downloader.services.exception import ValidationException


def download_page(url, output):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/80.0.3987.163 Safari/537.36'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(f'{output}/index.html', 'w') as file:
            file.write(response.text)
        return response.text
    else:
        raise ValidationException(f'Could not download main site from {url}')
