
def is_fb_pixel(image):
    if 'PageView' in image:
        return True
    return False


def is_url(input_value):
    if input_value.startswith('http'):
        return True
    return False
