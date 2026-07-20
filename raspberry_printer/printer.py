from datetime import datetime
import subprocess

from raspberry_printer.dither import DitherApply
from raspberry_printer.utils import set_bluetooth_config
from raspberry_printer.image import generate_image


def call_printer(serial_path, text, is_github_type=False, github_type='Issue'):
    img = generate_image(None, text)
    d = DitherApply(img.size, img.load())
    img_hex_str = d.make_image_hex_str()
    print('Starting print')
    ser = set_bluetooth_config(serial_path or '/dev/rfcomm1')
    hex_len = hex(int(len(img_hex_str) / 96) + 3)[2:]
    # little-endian for the length of hex lines
    front_hex = hex_len
    end_hex = '0'
    if len(hex_len) > 2:
        front_hex = hex_len[1:3]
        end_hex += hex_len[0:1]
    else:
        end_hex += '0'
    # start command with data length
    ser.write(
        bytes.fromhex(
            ('1D7630003000' + front_hex + end_hex).ljust(32, '0') + img_hex_str[0:224]
        )
    )
    # optional speaker call (kept for compatibility, disabled by default)
    now = datetime.now()
    if is_github_type and 8 < now.hour < 21:
        try:
            subprocess.check_output(
                ['micli', '5-3', f'哈哈哈哈哈，您有新的{github_type}请注意查收']
            )
        except Exception as e:
            print(f'Wrong call the speaker {str(e)}')
    # send the image data in chunks
    for i in range(32 * 7, len(img_hex_str), 256):
        chunk = img_hex_str[i : i + 256]
        if len(chunk) < 256:
            chunk = chunk.ljust(256, '0')
        ser.write(bytes.fromhex(chunk))
    print('Print is over')
