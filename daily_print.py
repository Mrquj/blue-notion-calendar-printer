import os
from dotenv import load_dotenv

from calendar_fetcher import fetch_today_events
from format_text import format_events
from raspberry_printer.printer import call_printer


def main():
    load_dotenv()
    serial_path = os.getenv('PRINTER_SERIAL_PATH', '/dev/rfcomm1')
    events = fetch_today_events()
    text = format_events(events)
    print(text)
    call_printer(serial_path, text)


if __name__ == '__main__':
    main()
