#!/usr/bin/env python3
"""
Claude Buddy installer.
Run: python install.py
Uninstall: python install.py --uninstall
"""

import json
import shutil
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PLUGIN_DIR   = Path(__file__).parent.parent
SCRIPTS_DIR  = PLUGIN_DIR / 'scripts'
CLAUDE_DIR   = Path.home() / '.claude'
SETTINGS     = CLAUDE_DIR / 'settings.json'
COMMANDS_DIR = CLAUDE_DIR / 'commands'
CONFIG       = PLUGIN_DIR / 'config.json'
SKILL_SRC    = PLUGIN_DIR / 'SKILL.md'
COMMAND_DST  = COMMANDS_DIR / 'buddy.md'

# Use 'python' so it matches however Claude Code resolves it on each platform.
# On Windows this works via PATH; on Mac/Linux use python3 if needed.
import platform
PYTHON_CMD = 'python' if platform.system() == 'Windows' else 'python3'

HOOK_CMD   = f'{PYTHON_CMD} {SCRIPTS_DIR / "generate_buddy.py"}'.replace('\\', '/')
BUDDY_SL   = f'{PYTHON_CMD} {SCRIPTS_DIR / "statusline_buddy.py"}'.replace('\\', '/')
COMBINED_SL = f'{PYTHON_CMD} {SCRIPTS_DIR / "statusline_combined.py"}'.replace('\\', '/')


def hook_has_buddy(h):
    if 'claude-buddy' in h.get('command', ''):
        return True
    for inner in h.get('hooks', []):
        if 'claude-buddy' in inner.get('command', ''):
            return True
    return False


def load_settings():
    if SETTINGS.exists():
        return json.loads(SETTINGS.read_text(encoding='utf-8'))
    return {}


def save_settings(data):
    backup = SETTINGS.with_suffix('.json.bak')
    if SETTINGS.exists():
        shutil.copy2(SETTINGS, backup)
        print(f"  Backup saved → {backup}")
    SETTINGS.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def install():
    print("\n╔══════════════════════════════════════╗")
    print("║    Claude Buddy — Installing  🦆     ║")
    print("╚══════════════════════════════════════╝\n")

    settings = load_settings()

    # ── 1. SessionStart hook ─────────────────────────────────────────────────
    hooks = settings.setdefault('hooks', {})
    session_hooks = hooks.get('SessionStart', [])
    if not isinstance(session_hooks, list):
        session_hooks = []

    already = any(hook_has_buddy(h) for h in session_hooks)
    if not already:
        session_hooks.append({
            'matcher': '*',
            'hooks': [{'type': 'command', 'command': HOOK_CMD}]
        })
        hooks['SessionStart'] = session_hooks
        print("  ✓ SessionStart hook added")
    else:
        print("  ✓ SessionStart hook already present (skipping)")

    # ── 2. Status line ───────────────────────────────────────────────────────
    existing_sl = settings.get('statusLine')
    existing_cmd = ''
    existing_padding = 0

    if isinstance(existing_sl, dict):
        existing_cmd = existing_sl.get('command', '')
        existing_padding = existing_sl.get('padding', 0)

    if not existing_cmd or 'claude-buddy' in existing_cmd:
        # No previous status line (or already ours) → just use buddy
        settings['statusLine'] = {
            'type': 'command',
            'command': BUDDY_SL,
            'padding': existing_padding,
        }
        print("  ✓ Status line set → buddy")
    else:
        # Previous status line exists → save it and use combined wrapper
        cfg = {'previous_statusline_command': existing_cmd}
        CONFIG.write_text(json.dumps(cfg, indent=2), encoding='utf-8')
        settings['statusLine'] = {
            'type': 'command',
            'command': COMBINED_SL,
            'padding': existing_padding,
        }
        print(f"  ✓ Previous status line detected: {existing_cmd}")
        print("  ✓ Status line set → combined (previous + buddy)")

    save_settings(settings)

    # ── 3. /buddy slash command ──────────────────────────────────────────────
    COMMANDS_DIR.mkdir(exist_ok=True)
    shutil.copy2(SKILL_SRC, COMMAND_DST)
    print("  ✓ /buddy command registered")

    print("\n╔══════════════════════════════════════╗")
    print("║  Done! Restart Claude Code to meet  ║")
    print("║  your first session buddy.  ★        ║")
    print("╚══════════════════════════════════════╝\n")


def uninstall():
    print("\n  Removing Claude Buddy...\n")
    settings = load_settings()

    # Remove hook
    hooks = settings.get('hooks', {})
    session_hooks = hooks.get('SessionStart', [])
    if isinstance(session_hooks, list):
        filtered = [h for h in session_hooks if not hook_has_buddy(h)]
        if filtered:
            hooks['SessionStart'] = filtered
        else:
            hooks.pop('SessionStart', None)
    print("  ✓ SessionStart hook removed")

    # Restore previous status line
    prev_cmd = ''
    if CONFIG.exists():
        try:
            cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
            prev_cmd = cfg.get('previous_statusline_command', '')
        except Exception:
            pass

    if prev_cmd:
        settings['statusLine'] = {'type': 'command', 'command': prev_cmd, 'padding': 0}
        print(f"  ✓ Status line restored → {prev_cmd}")
    else:
        settings.pop('statusLine', None)
        print("  ✓ Status line removed")

    save_settings(settings)

    # Remove /buddy command
    if COMMAND_DST.exists():
        COMMAND_DST.unlink()
        print("  ✓ /buddy command removed")

    print("\n  Claude Buddy uninstalled. Goodbye. 👋\n")


if __name__ == '__main__':
    if '--uninstall' in sys.argv:
        uninstall()
    else:
        install()
