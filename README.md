# blue-notion-calendar-printer

基于 [yihong0618/blue](https://github.com/yihong0618/blue) 项目改造，**每天定时**把 Notion Calendar 中已勾选的日历事件/任务打印到蓝牙热敏打印机。

> 原项目 `uuavv/blue` 保持不变，本项目是一个独立的新仓库。

## 设计思路

- 在树莓派上通过 `cron` 每天定时运行 `daily_print.py`。
- 脚本读取 `.env` 中配置的日历 ICS 订阅链接，拉取今日事件。
- 事件按时间排序、格式化为文本，调用原项目的蓝牙热敏打印机驱动打印。

## ⚠️ 关于“Notion Calendar 已勾选日历”

Notion Calendar 目前**不对外开放**“已勾选日历列表”的读取 API，因此本项目采用**ICS 订阅链接**作为数据源。  
你只需在 Notion Calendar 里勾选想要的日历，然后把这些日历的 **ICS 地址**复制到 `.env` 的 `CALENDAR_ICS_URLS` 中即可。后续在 Notion 中增减勾选时，同步更新 `.env` 里的链接列表。

## 硬件要求

- 树莓派（带蓝牙，3B+ 及以上）
- 蓝牙热敏打印机（与原项目相同）
- 已配对并建立 `rfcomm` 连接，例如 `/dev/rfcomm1`

## 快速开始

1. 克隆仓库
   ```bash
   git clone https://github.com/Mrquj/blue-notion-calendar-printer.git
   cd blue-notion-calendar-printer
   ```

2. 创建虚拟环境并安装依赖
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. 下载/准备字体
   ```bash
   python setup.py
   ```
   如果下载失败，请手动从原项目复制 `resources/zpix.ttf` 到本项目的 `resources/` 目录。

4. 配置环境变量
   ```bash
   cp .env.example .env
   # 编辑 .env，填入 PRINTER_SERIAL_PATH、TIMEZONE、CALENDAR_ICS_URLS
   ```

5. 手动运行一次，确认打印正常
   ```bash
   python daily_print.py
   ```

6. 加入 cron
   ```bash
   crontab crontab.example
   ```

## 获取 ICS 链接

- **iCloud**：在 `calendar.icloud.com` 中右键日历 → 共享日历 → 公开日历 → 复制 URL。
- **Google Calendar**：日历设置 → 集成日历 → 公开地址（ICAL）/ 私密地址（ICAL）。
- **Outlook**：日历 → 共享 → 发布此日历 → 获取 ICS 链接。

## 配置说明

| 环境变量 | 说明 | 默认值 |
|---|---|---|
| `PRINTER_SERIAL_PATH` | 蓝牙打印机串口路径 | `/dev/rfcomm1` |
| `TIMEZONE` | 时区 | `Asia/Shanghai` |
| `CALENDAR_ICS_URLS` | 已勾选日历的 ICS 链接，多个用英文逗号分隔 | 空 |
| `LOCAL_ICS_FILES` | 本地 `.ics` 文件路径，多个用英文逗号分隔 | 空 |
| `FONT_RESOURCE` | 中文字体路径 | `resources/zpix.ttf` |

## 文件结构

```
blue-notion-calendar-printer/
├── daily_print.py          # 入口：拉取日历并打印
├── calendar_fetcher.py     # ICS 拉取与解析
├── format_text.py          # 文本格式化
├── raspberry_printer/      # 打印机驱动（来自 blue）
│   ├── printer.py
│   ├── image.py
│   ├── dither.py
│   ├── utils.py
│   └── config.py
├── setup.py                # 下载字体
├── requirements.txt
├── .env.example
├── crontab.example
└── README.md
```

## 许可证

与原项目相同，MIT License。
