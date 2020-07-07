
def is_fb_pixel(image):
    if 'PageView' in image:
        return True
    return False


def is_url(input_value):
    if input_value.startswith('http'):
        return True
    return False


def is_google_font(input_value):
    if 'fonts.googleapis.com' in input_value:
        return True
    return False


def is_google_tag_manager(input_value):
    if 'googletagmanager.com' in input_value:
        return True
    return False


def is_favicon(input_value):
    if 'favicon' in input_value:
        return True
    return False


def file_loader(filename, binary=False):
    """Loads data from file"""
    read_option = 'r'
    if binary:
        read_option = 'rb'

    with open(filename, read_option) as f:
        data = f.read()

    return data
