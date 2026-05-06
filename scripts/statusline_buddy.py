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
    'COMMON':    '\033[97m',
    'UNCOMMON':  '\033[92m',
    'RARE':      '\033[96m',
    'EPIC':      '\033[95m',
    'LEGENDARY': '\033[93m',
}

STAGE_THRESHOLDS = [0, 500_000, 1_000_000, 5_000_000, 10_000_000]


def fmt_tokens(n: int) -> str:
    if n >= 1_000_000:
        return f'{n/1_000_000:.1f}M'
    if n >= 1_000:
        return f'{n/1_000:.0f}K'
    return str(n)


def main() -> None:
    session_path   = Path.home() / '.claude' / 'buddy_session.json'
    evolution_path = Path.home() / '.claude' / 'buddy_evolution.json'

    if not session_path.exists():
        return

    try:
        buddy = json.loads(session_path.read_text(encoding='utf-8-sig'))
    except (json.JSONDecodeError, OSError):
        return

    evolution = None
    if evolution_path.exists():
        try:
            evolution = json.loads(evolution_path.read_text(encoding='utf-8-sig'))
        except (json.JSONDecodeError, OSError):
            pass

    rarity  = buddy.get('rarity', 'COMMON')
    col     = ANSI.get(rarity, ANSI['COMMON'])
    bold    = ANSI['bold']
    reset   = ANSI['reset']
    dim     = ANSI['dim']

    emoji    = buddy.get('emoji', '?')
    name     = buddy.get('name', '???')
    stars    = buddy.get('stars', '★')
    shiny    = '✨' if buddy.get('shiny') else ''
    peak     = buddy.get('peak_stat', '')
    peak_val = buddy.get('stats', {}).get(peak, 0)

    shiny_part = f' {shiny}' if shiny else ''
    peak_part  = f'  {dim}{peak[:3]} {peak_val}{reset}' if peak else ''

    token_part = ''
    if evolution:
        tokens = evolution.get('tokens_total', 0)
        stage  = evolution.get('evolution_stage', 0)
        if stage < len(STAGE_THRESHOLDS) - 1:
            next_threshold = STAGE_THRESHOLDS[stage + 1]
            token_part = f'  {dim}S{stage} {fmt_tokens(tokens)}→{fmt_tokens(next_threshold)}{reset}'
        else:
            token_part = f'  {dim}S{stage} {fmt_tokens(tokens)} MAX{reset}'

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
        f"{token_part}"
        f"{phrase_part}"
    )

    print(line)


if __name__ == '__main__':
    main()
