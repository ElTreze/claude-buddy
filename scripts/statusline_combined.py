#!/usr/bin/env python3
"""
Combined status line: existing command + buddy.
The installer writes the previous statusLine command to config.json.
"""

import json
import subprocess
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CONFIG_PATH = Path(__file__).parent.parent / 'config.json'
BUDDY_SCRIPT = Path(__file__).parent / 'statusline_buddy.py'
PYTHON = sys.executable


def run_script(script):
    try:
        r = subprocess.run(
            [PYTHON, str(script)],
            capture_output=True, text=True, timeout=3,
            encoding='utf-8', errors='replace',
        )
        return r.stdout.strip()
    except Exception:
        return ''


def run_command(cmd):
    try:
        r = subprocess.run(
            cmd, shell=True,
            capture_output=True, text=True, timeout=3,
            encoding='utf-8', errors='replace',
        )
        return r.stdout.strip()
    except Exception:
        return ''


def main():
    prev_cmd = ''
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
            prev_cmd = cfg.get('previous_statusline_command', '')
        except Exception:
            pass

    buddy = run_script(BUDDY_SCRIPT)
    prev  = run_command(prev_cmd) if prev_cmd else ''

    sep = '  \033[90m│\033[0m  '

    if prev and buddy:
        print(f"{prev}{sep}{buddy}")
    elif buddy:
        print(buddy)
    elif prev:
        print(prev)


if __name__ == '__main__':
    main()
