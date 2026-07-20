from datetime import datetime


def format_events(events):
    now = datetime.now()
    lines = [
        '今日 Notion Calendar 任务清单',
        now.strftime('%Y-%m-%d %H:%M'),
        '-' * 27,
        ''
    ]
    if not events:
        lines.append('今天没有日历事件/任务。')
        lines.append('')
        lines.append('-' * 27)
        return chr(10).join(lines)
    for i, ev in enumerate(events, 1):
        start = ev['start']
        end = ev['end']
        if start.date() == end.date():
            time_str = f'{start.strftime("%H:%M")}-{end.strftime("%H:%M")}'
        else:
            time_str = f'{start.strftime("%m-%d %H:%M")}-{end.strftime("%m-%d %H:%M")}'
        lines.append(f'{i}. {time_str} {ev["summary"]}')
        desc = ev['description'].strip()
        if desc:
            desc = desc.replace(chr(10), ' ')[:80]
            lines.append(f'   {desc}')
        loc = ev['location'].strip()
        if loc:
            lines.append(f'   @ {loc}')
        lines.append('')
    lines.append(f'共 {len(events)} 项')
    lines.append('-' * 27)
    return chr(10).join(lines)
