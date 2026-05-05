#!/usr/bin/env python3
"""
Claude Buddy - Status line renderer
Outputs compact buddy info with ANSI colors for the status bar.
"""

import json
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ANSI = {
    'reset':     '\033[0m',
    'bold':      '\033[1m',
    'dim':       '\033[2m',
    'COMMON':    '\033[97m',   # white
    'UNCOMMON':  '\033[92m',   # green
    'RARE':      '\033[96m',   # cyan
    'EPIC':      '\033[95m',   # magenta
    'LEGENDARY': '\033[93m',   # gold/yellow
}


def main():
    session_path = Path.home() / '.claude' / 'buddy_session.json'

    if not session_path.exists():
        return

    try:
        buddy = json.loads(session_path.read_text(encoding='utf-8'))
    except Exception:
        return

    rarity  = buddy.get('rarity', 'COMMON')
    col     = ANSI.get(rarity, ANSI['COMMON'])
    bold    = ANSI['bold']
    reset   = ANSI['reset']
    dim     = ANSI['dim']

    emoji   = buddy.get('emoji', '?')
    name    = buddy.get('name', '???')
    stars   = buddy.get('stars', '★')
    shiny   = '✨' if buddy.get('shiny') else ''
    peak    = buddy.get('peak_stat', '')
    peak_val = buddy.get('stats', {}).get(peak, 0)

    shiny_part = f' {shiny}' if shiny else ''
    peak_part  = f'  {dim}{peak[:3]} {peak_val}{reset}' if peak else ''

    personality = buddy.get('personality', '')
    if personality:
        phrase = personality if len(personality) <= 55 else personality[:52] + '...'
        phrase_part = f'  {dim}"{phrase}"{reset}'
    else:
        phrase_part = ''

    line = (
        f"{col}{bold}{emoji} {name}{reset}"
        f"  {col}{stars} {rarity}{shiny_part}{reset}"
        f"{peak_part}"
        f"{phrase_part}"
    )

    print(line)


if __name__ == '__main__':
    main()
