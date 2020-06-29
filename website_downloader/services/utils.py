
def is_fb_pixel(image):
    if 'PageView' in image:
        return True
    return False


def is_url(input_value):
    if input_value.startswith('http'):
        return True
    return False


def is_google_font(input_value):
    if input_value.startswith('https://fonts.googleapis.com'):
        return True
    return False


def is_favicon(input_value):
    if 'favicon' in input_value:
        return True
    return False
