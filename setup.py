import os
import urllib.request

FONT_RESOURCE = os.environ.get('FONT_RESOURCE', 'resources/zpix.ttf')
FONT_URL = 'https://raw.githubusercontent.com/yihong0618/blue/main/resources/zpix.ttf'


def main():
    if os.path.exists(FONT_RESOURCE):
        print(f'字体已存在：{FONT_RESOURCE}')
        return
    os.makedirs(os.path.dirname(FONT_RESOURCE) or '.', exist_ok=True)
    print(f'正在下载字体：{FONT_URL}')
    urllib.request.urlretrieve(FONT_URL, FONT_RESOURCE)
    print(f'字体已保存到：{FONT_RESOURCE}')


if __name__ == '__main__':
    main()
