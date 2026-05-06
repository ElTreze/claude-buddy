#!/usr/bin/env python3
"""
Claude Buddy - Stop hook
Reads transcript_path from stdin, counts output tokens, updates evolution.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Reconfigure stdin to strip UTF-8 BOM — PowerShell pipes add one on Windows
sys.stdin = open(sys.stdin.fileno(), encoding='utf-8-sig', errors='replace', closefd=False)

EVOLUTION_PATH = Path.home() / '.claude' / 'buddy_evolution.json'

RARITY_ORDER = ['COMMON', 'UNCOMMON', 'RARE', 'EPIC', 'LEGENDARY']
STARS_ORDER  = ['★', '★★', '★★★', '★★★★', '★★★★★']

STAGES = [
    {'threshold':           0, 'stat_boost':  0, 'rarity_up': False, 'shiny': False, 'force_legendary': False},
    {'threshold':  25_000_000, 'stat_boost': 10, 'rarity_up': False, 'shiny': False, 'force_legendary': False},
    {'threshold':  75_000_000, 'stat_boost': 10, 'rarity_up': True,  'shiny': False, 'force_legendary': False},
    {'threshold': 200_000_000, 'stat_boost': 15, 'rarity_up': True,  'shiny': True,  'force_legendary': False},
    {'threshold': 500_000_000, 'stat_boost': 20, 'rarity_up': False, 'shiny': True,  'force_legendary': True},
]


def count_session_tokens(transcript_path: str) -> int:
    """Sum output_tokens from all entries in the session transcript."""
    total = 0
    try:
        with open(transcript_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                usage = entry.get('usage') or (
                    entry.get('message', {}).get('usage') if isinstance(entry.get('message'), dict) else None
                )
                if usage and isinstance(usage, dict):
                    out = usage.get('output_tokens', 0)
                    if isinstance(out, int) and out > 0:
                        total += out
    except Exception:
        pass
    return total


def apply_evolution(evolution: dict) -> tuple[dict, bool]:
    """Check thresholds and apply any pending stage upgrades. Returns (updated_evolution, did_evolve)."""
    tokens = evolution['tokens_total']
    current_stage = evolution['evolution_stage']
    buddy = evolution['buddy']
    did_evolve = False

    for stage_idx in range(current_stage + 1, len(STAGES)):
        stage = STAGES[stage_idx]
        if tokens < stage['threshold']:
            break

        # Boost stats
        if stage['stat_boost'] > 0:
            new_stats = {
                k: min(100, v + stage['stat_boost'])
                for k, v in buddy['stats'].items()
            }
            buddy = {
                **buddy,
                'stats': new_stats,
                'peak_stat': max(new_stats, key=new_stats.get),
                'dump_stat': min(new_stats, key=new_stats.get),
            }

        # Rarity upgrade
        if stage['rarity_up']:
            rarity_idx = next((i for i, v in enumerate(RARITY_ORDER) if v == buddy['rarity']), 0)
            new_idx = min(rarity_idx + 1, len(RARITY_ORDER) - 1)
            buddy = {**buddy, 'rarity': RARITY_ORDER[new_idx], 'stars': STARS_ORDER[new_idx]}

        # Force legendary
        if stage['force_legendary']:
            buddy = {**buddy, 'rarity': 'LEGENDARY', 'stars': '★★★★★'}

        # Stars +1 on stage 1 (no rarity_up at that stage)
        if stage_idx == 1:
            stars_idx = next((i for i, v in enumerate(STARS_ORDER) if v == buddy['stars']), 0)
            new_idx = min(stars_idx + 1, len(STARS_ORDER) - 1)
            buddy = {**buddy, 'stars': STARS_ORDER[new_idx]}

        # Shiny
        if stage['shiny']:
            buddy = {**buddy, 'shiny': True}

        evolution = {**evolution, 'evolution_stage': stage_idx, 'buddy': buddy,
                     'evolved_at': [*evolution['evolved_at'], datetime.now().isoformat()]}
        did_evolve = True

    return evolution, did_evolve


def main() -> None:
    try:
        stdin_data = json.loads(sys.stdin.read())
    except Exception:
        return

    transcript_path = stdin_data.get('transcript_path', '')
    if not transcript_path:
        return

    session_tokens = count_session_tokens(transcript_path)
    if session_tokens == 0:
        return

    if not EVOLUTION_PATH.exists():
        return

    try:
        raw = EVOLUTION_PATH.read_text(encoding='utf-8-sig')  # utf-8-sig strips BOM if present
        evolution = json.loads(raw)
    except (json.JSONDecodeError, OSError, IOError):
        return
    tokens_before = evolution.get('tokens_total', 0)
    level_before  = min(10000, tokens_before // 1_000_000 + 1)

    evolution = {
        **evolution,
        'tokens_total': tokens_before + session_tokens,
        'sessions': evolution.get('sessions', 0) + 1,
    }

    evolution, did_evolve = apply_evolution(evolution)

    tokens_after = evolution['tokens_total']
    level_after  = min(10000, tokens_after // 1_000_000 + 1)

    try:
        EVOLUTION_PATH.write_text(
            json.dumps(evolution, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    except Exception:
        return

    session_path = Path.home() / '.claude' / 'buddy_session.json'
    buddy_with_level = {**evolution['buddy'], 'level': level_after}
    try:
        session_path.write_text(
            json.dumps(buddy_with_level, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    except Exception:
        return

    if did_evolve:
        stage = evolution['evolution_stage']
        tokens_m = tokens_after / 1_000_000
        print(json.dumps({
            "systemMessage": f"✨ {evolution['buddy']['name']} evolved to Stage {stage}! Now lvl. {level_after} ({tokens_m:.1f}M tokens)"
        }))
    else:
        # Notify on every 25-level milestone
        prev_milestone = (level_before - 1) // 25
        curr_milestone = (level_after  - 1) // 25
        if curr_milestone > prev_milestone and level_after > 1:
            milestone_lvl = curr_milestone * 25
            print(json.dumps({
                "systemMessage": f"🎉 {evolution['buddy']['name']} reached lvl. {milestone_lvl}!"
            }))


if __name__ == '__main__':
    main()
