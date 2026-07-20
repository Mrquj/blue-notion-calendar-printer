import os
from datetime import datetime, timedelta, timezone

import requests
from icalendar import Calendar
from recurring_ical_events import of
from dateutil.tz import gettz


def _get_today_bounds(tz):
    now = datetime.now(tz)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end


def _load_ics_from_url(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return Calendar.from_ical(response.text)


def _load_ics_from_path(path):
    with open(path, 'rb') as f:
        return Calendar.from_ical(f.read())


def _events_from_calendar(cal, start, end):
    return list(of(cal).between(start, end))


def _normalize_event(ev, tz):
    start = ev.start
    end = ev.end
    if isinstance(start, datetime):
        start = start.astimezone(tz)
    else:
        start = datetime.combine(start, datetime.min.time(), tzinfo=tz)
    if isinstance(end, datetime):
        end = end.astimezone(tz)
    else:
        end = datetime.combine(end, datetime.min.time(), tzinfo=tz) + timedelta(days=1)
    return {
        'summary': str(ev.get('summary', '')),
        'description': str(ev.get('description', '')),
        'location': str(ev.get('location', '')),
        'start': start,
        'end': end,
    }


def fetch_today_events():
    tz_name = os.getenv('TIMEZONE', 'Asia/Shanghai')
    tz = gettz(tz_name)
    if tz is None:
        tz = timezone(timedelta(hours=8))
    start, end = _get_today_bounds(tz)
    events = []
    urls = [u.strip() for u in os.getenv('CALENDAR_ICS_URLS', '').split(',') if u.strip()]
    for url in urls:
        try:
            cal = _load_ics_from_url(url)
            events.extend(_events_from_calendar(cal, start, end))
        except Exception as e:
            print(f'无法获取日历 {url}: {e}')
    local_files = [p.strip() for p in os.getenv('LOCAL_ICS_FILES', '').split(',') if p.strip()]
    for path in local_files:
        try:
            cal = _load_ics_from_path(path)
            events.extend(_events_from_calendar(cal, start, end))
        except Exception as e:
            print(f'无法读取本地文件 {path}: {e}')
    normalized = [_normalize_event(ev, tz) for ev in events]
    normalized.sort(key=lambda x: x['start'])
    return normalized
