from PIL import Image, ImageFont, ImageDraw
from raspberry_printer.config import FONT_RESOURCE, WIDTH


def generate_image(src, text, font=FONT_RESOURCE):
    """
    base function from https://github.com/j178 great thanks
    """
    if src is not None:
        img = Image.open(src)
    elif text is not None:
        # add ----- in front and end
        text = '-' * 27 + chr(10) + text + chr(10)
        text = text + ' ' * 27 * 5
        font_size = 20
        font = ImageFont.truetype(FONT_RESOURCE, font_size)
        content = ''
        line_length = 0
        for c in text:
            if c == chr(10):
                line_length = 0
                content += chr(10)
                continue
            elif ord(c) <= 256:
                l = 0.5
            else:
                l = 1
            if line_length + l > WIDTH // font_size - 2:
                content += chr(10)
                line_length = 0
            line_length += l
            content += c

        line_cnt = content.count(chr(10)) + 1
        img = Image.new('RGB', (WIDTH, (font_size + 2) * line_cnt), 'white')
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), str(content), fill='black', font=font)
    else:
        raise Exception('Either src or text must be provided')
    return img
