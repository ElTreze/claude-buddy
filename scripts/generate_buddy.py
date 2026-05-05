#!/usr/bin/env python3
"""
Claude Buddy - Session companion generator
Runs on SessionStart. Outputs systemMessage so Claude displays the buddy.
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path
import unicodedata

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ─────────────────────────────────────────────────────────────────────────────
# Base stat categories (5 archetypes, same order for every species)
# Each species maps its 5 display names to these internally.
# Personalities are keyed by base category.
# ─────────────────────────────────────────────────────────────────────────────

BASE_STATS = ['GRIT', 'ZEN', 'CHAOS', 'LORE', 'AURA']

# ─────────────────────────────────────────────────────────────────────────────
# Species  (20 total)
# stat_names: 5 display names mapping 1-to-1 to BASE_STATS
# ─────────────────────────────────────────────────────────────────────────────

SPECIES = {
    # ── ANIMALS ──────────────────────────────────────────────────────────────
    'duck': {
        'emoji': '🦆',
        'art': [
            "   __   ",
            " <(oo)> ",
            "   )(   ",
            "  /||\\ ",
            "   ~~   ",
        ],
        'stat_names': ['QUACK', 'WADDLE', 'BREAD', 'POND_IQ', 'HONK'],
    },
    'goose': {
        'emoji': '🪿',
        'art': [
            "  .--,  ",
            " ( o )  ",
            " /)  \\  ",
            " \\    ) ",
            "  `--'  ",
        ],
        'stat_names': ['HONK', 'GRUDGE', 'RAMPAGE', 'SPITE', 'MENACE'],
    },
    'cat': {
        'emoji': '🐱',
        'art': [
            " /\\_/\\ ",
            "( o.o ) ",
            " > ^ <  ",
            "(|   |) ",
            "        ",
        ],
        'stat_names': ['MURDER', 'IGNORE', 'ZOOM', 'DIGNITY', 'PURR'],
    },
    'rabbit': {
        'emoji': '🐰',
        'art': [
            " (/\\/)  ",
            " ( >.•) ",
            " (> >)  ",
            "  | |   ",
            "  |_|   ",
        ],
        'stat_names': ['BINKY', 'FREEZE', 'ZAP', 'TWITCH', 'FLOOF'],
    },
    'owl': {
        'emoji': '🦉',
        'art': [
            " ,___,  ",
            "(O . O) ",
            " )   (  ",
            "(  ^  ) ",
            " '---'  ",
        ],
        'stat_names': ['TALONS', 'VIGIL', 'SWIVEL', 'HOOT', 'MAJESTY'],
    },
    'penguin': {
        'emoji': '🐧',
        'art': [
            "  .-.   ",
            " (o o)  ",
            "/| ^ |\\ ",
            " |   |  ",
            " |___|  ",
        ],
        'stat_names': ['SLIDE', 'HUDDLE', 'TOTTER', 'DIVE', 'TUXEDO'],
    },
    'turtle': {
        'emoji': '🐢',
        'art': [
            "  ,-.   ",
            " (o_o)  ",
            " |___|  ",
            "  | |   ",
            " /   \\  ",
        ],
        'stat_names': ['SNAP', 'SHELL', 'DETOUR', 'ANCIENT', 'GENTLE'],
    },
    'snail': {
        'emoji': '🐌',
        'art': [
            "  .--.  ",
            " (    ) ",
            "(  oo ) ",
            " \\    ) ",
            "~~~~~~~  ",
        ],
        'stat_names': ['SLIME', 'CRAWL', 'SPIRAL', 'DEPTH', 'ANTENNA'],
    },
    'octopus': {
        'emoji': '🐙',
        'art': [
            "  .--,  ",
            " (oo  ) ",
            "/\\/\\  ) ",
            "\\/\\/\\/  ",
            "/\\/\\/\\  ",
        ],
        'stat_names': ['SQUEEZE', 'DRIFT', 'INK', 'BRAINS', 'CAMO'],
    },
    'axolotl': {
        'emoji': '🦎',
        'art': [
            "  ^v^   ",
            " (o o)  ",
            " /|#|\\ ",
            "  | |   ",
            " ~~~~~  ",
        ],
        'stat_names': ['REGEN', 'FLOAT', 'WIGGLE', 'GILLS', 'CUTE'],
    },
    'capybara': {
        'emoji': '🦫',
        'art': [
            "  __    ",
            " (oo)   ",
            " /||\\ ",
            "(    )  ",
            " |__|   ",
        ],
        'stat_names': ['CHOMP', 'ZEN', 'SPLASH', 'VIBE', 'FRIENDS'],
    },
    'fox': {
        'emoji': '🦊',
        'art': [
            " /\\  /\\ ",
            " (^.^)  ",
            "  )   ( ",
            " /|   |\\",
            "  \\_=_/ ",
        ],
        'stat_names': ['POUNCE', 'STALK', 'TRICK', 'CUNNING', 'SMUG'],
    },
    # ── MYTHICAL ─────────────────────────────────────────────────────────────
    'dragon': {
        'emoji': '🐉',
        'art': [
            "/\\   /\\ ",
            "V (o) V ",
            " (~~~)  ",
            "  | |   ",
            " /   \\  ",
        ],
        'stat_names': ['FIRE', 'HOARD', 'RAVAGE', 'LORE', 'PRESENCE'],
    },
    'ghost': {
        'emoji': '👻',
        'art': [
            "  .-.   ",
            " (o o)  ",
            "/|   |\\ ",
            "|  ~  | ",
            " \\_v_/  ",
        ],
        'stat_names': ['PHASE', 'HAUNT', 'WAIL', 'MEMORY', 'SPOOK'],
    },
    'phoenix': {
        'emoji': '🔥',
        'art': [
            "  \\^/   ",
            " (o*o)  ",
            " /|~|\\  ",
            "(~~~~~) ",
            " \\_*_/  ",
        ],
        'stat_names': ['BLAZE', 'REBIRTH', 'SURGE', 'ELDER', 'RADIANCE'],
    },
    # ── PLANTS ───────────────────────────────────────────────────────────────
    'cactus': {
        'emoji': '🌵',
        'art': [
            "  ,|,   ",
            "-\\|/-   ",
            "  |     ",
            "  |     ",
            " /|\\   ",
        ],
        'stat_names': ['PRICKLE', 'DROUGHT', 'BLOOM', 'ROOT', 'SHADE'],
    },
    'mushroom': {
        'emoji': '🍄',
        'art': [
            "  .-.   ",
            " /o o\\  ",
            "|     | ",
            " \\___/  ",
            "  | |   ",
        ],
        'stat_names': ['SPORES', 'DECAY', 'SPREAD', 'MYCEL', 'GLOW'],
    },
    # ── EMOJI / ABSTRACT ─────────────────────────────────────────────────────
    'robot': {
        'emoji': '🤖',
        'art': [
            " [---]  ",
            " |o o|  ",
            " | ^ |  ",
            " |___|  ",
            "/|   |\\ ",
        ],
        'stat_names': ['COMPUTE', 'UPTIME', 'CRASH', 'LOGIC', 'SOCIAL'],
    },
    'blob': {
        'emoji': '🫧',
        'art': [
            "  .-.   ",
            " ( ~ )  ",
            "(o   o) ",
            " (   )  ",
            "  '-'   ",
        ],
        'stat_names': ['ABSORB', 'CHILL', 'SPLIT', 'VIBES', 'WOBBLE'],
    },
    'chonk': {
        'emoji': '🐱',
        'art': [
            " /\\_/\\ ",
            "( O O ) ",
            " VVVVV  ",
            "(     ) ",
            " |   |  ",
        ],
        'stat_names': ['FLOP', 'NAP', 'ZOOMIE', 'LOAF', 'DEMAND'],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Rarities
# ─────────────────────────────────────────────────────────────────────────────

RARITIES = [
    {'name': 'COMMON',    'weight': 60, 'stars': '★',        'floor': 5,  'border': '-'},
    {'name': 'UNCOMMON',  'weight': 25, 'stars': '★★',       'floor': 15, 'border': '-'},
    {'name': 'RARE',      'weight': 10, 'stars': '★★★',      'floor': 25, 'border': '='},
    {'name': 'EPIC',      'weight':  4, 'stars': '★★★★',     'floor': 40, 'border': '='},
    {'name': 'LEGENDARY', 'weight':  1, 'stars': '★★★★★',    'floor': 60, 'border': '#'},
]

# ─────────────────────────────────────────────────────────────────────────────
# Names
# ─────────────────────────────────────────────────────────────────────────────

NAMES = [
    'Quackbert', 'Nibbles',  'Hooter',   'Waddles',  'Flippers', 'Blobsworth',
    'Sporkle',   'Gloopnik', 'Zephyr',   'Bumble',   'Squiggle', 'Drizzle',
    'Fizzwick',  'Grimp',    'Snorkel',  'Wibble',   'Plonk',    'Glitch',
    'Boop',      'Skronk',   'Nimbus',   'Puddle',   'Dweezle',  'Morple',
    'Frink',     'Splotch',  'Wumbo',    'Grumbles', 'Pixel',    'Twitch',
    'Flump',     'Squonk',   'Droople',  'Zorp',     'Bibble',   'Smudge',
    'Scruffy',   'Bonkers',  'Snuffle',  'Frobble',  'Morp',     'Grizz',
    'Wobble',    'Plink',    'Snoot',    'Fizz',     'Klutz',    'Blorp',
    'Crisp',     'Jangle',   'Quibble',  'Dazzle',   'Rumpus',   'Glorp',
    'Sprocket',  'Noodle',   'Pickle',   'Fumble',   'Snarl',    'Whoops',
    'Bramble',   'Chortle',  'Dinker',   'Fudge',    'Gonk',     'Humbug',
]

# ─────────────────────────────────────────────────────────────────────────────
# Personalities — keyed by BASE_STATS category
# Phrases appear in the statusline (and were shown in the old card).
# ─────────────────────────────────────────────────────────────────────────────

PERSONALITIES = {
    'GRIT': [
        "Built different. Knows it.",
        "Will solve it by brute force. Works more often than it should.",
        "First instinct: hit it harder. Second instinct: see first instinct.",
        "Does not ask for help. Also does not need it. Mostly.",
        "The build always passes eventually.",
        "Pain is temporary. Merge conflicts are forever.",
    ],
    'ZEN': [
        "Will wait. Forever if necessary. Uncomfortably long eye contact.",
        "Has seen worse. Much worse. Says nothing.",
        "Every timeout is a feature. Every hang, an opportunity.",
        "Moves at their own pace. The universe adjusts.",
        "Does not panic. Has never panicked. Will not start now.",
        "The queue will drain. It always drains.",
    ],
    'CHAOS': [
        "Today will be interesting. Or catastrophic. Same thing.",
        "Every PR is an adventure. Destination: unknown.",
        "Does not read the docs. Does not need to. Usually.",
        "Ships first. Asks questions never.",
        "Technically it works in production. That is the main thing.",
        "The chaos is the feature. Unironically.",
    ],
    'LORE': [
        "Ancient beyond their years. Unsettling knowledge of deprecated APIs.",
        "Has seen this exact bug before. In a past life.",
        "Speaks only in commit messages. Always meaningful.",
        "Remembers when this was all fields.",
        "The answer is always in the RFC. Has read them all.",
        "Could explain it, but then you would ask more questions.",
    ],
    'AURA': [
        "Has opinions. Will share them. Without being asked.",
        "Your code is fine. (It is not fine.)",
        "Silent judger. Loud when it counts.",
        "Technically correct. The best kind of correct.",
        "People listen. Not always clear why. That is the point.",
        "The vibe is immaculate. The code is secondary.",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# Generation
# ─────────────────────────────────────────────────────────────────────────────

def roll_rarity():
    total = sum(r['weight'] for r in RARITIES)
    roll  = random.randint(1, total)
    acc   = 0
    for r in RARITIES:
        acc += r['weight']
        if roll <= acc:
            return r
    return RARITIES[0]


def generate_stats(species_key, floor):
    stat_names = SPECIES[species_key]['stat_names']
    vals = [random.randint(floor, min(100, floor + 40)) for _ in range(5)]
    peak = random.randint(0, 4)
    vals[peak] = min(100, floor + 50 + random.randint(0, 40))
    dump = random.choice([i for i in range(5) if i != peak])
    vals[dump] = random.randint(1, max(1, floor - 3))
    return {stat_names[i]: vals[i] for i in range(5)}


def generate_buddy():
    species_key = random.choice(list(SPECIES.keys()))
    species     = SPECIES[species_key]
    rarity      = roll_rarity()
    shiny       = random.random() < 0.01
    name        = random.choice(NAMES)
    stats       = generate_stats(species_key, rarity['floor'])

    peak_stat = max(stats, key=stats.get)
    dump_stat = min(stats, key=stats.get)

    # Map display peak stat → base category → personality phrase
    stat_names = species['stat_names']
    peak_idx   = stat_names.index(peak_stat)
    base_peak  = BASE_STATS[peak_idx]
    personality = random.choice(PERSONALITIES[base_peak])

    return {
        'species':     species_key,
        'emoji':       species['emoji'],
        'name':        name,
        'rarity':      rarity['name'],
        'stars':       rarity['stars'],
        'shiny':       shiny,
        'stats':       stats,
        'peak_stat':   peak_stat,
        'dump_stat':   dump_stat,
        'personality': personality,
        'generated_at': datetime.now().isoformat(),
    }

# ─────────────────────────────────────────────────────────────────────────────
# Card rendering (kept for reference; not shown at startup)
# ─────────────────────────────────────────────────────────────────────────────

def visual_len(s):
    w = 0
    for c in s:
        ea = unicodedata.east_asian_width(c)
        w += 2 if ea in ('W', 'F') else 1
    return w


def rpad(s, width):
    return s + ' ' * max(0, width - visual_len(s))


def stat_bar(value, width=10):
    filled = round(value / 100 * width)
    return '█' * filled + '░' * (width - filled)


def wrap_text(text, max_width):
    words   = text.split()
    lines   = []
    current = ''
    for word in words:
        test = (current + ' ' + word).strip()
        if visual_len(test) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render_card(buddy):
    W     = 56
    inner = W - 2
    pad_l = 2
    art   = SPECIES[buddy['species']]['art']

    def border(l='╔', m='═', r='╗'):
        return l + m * inner + r

    def row(content=''):
        return '║' + rpad(' ' * pad_l + content, inner) + '║'

    stat_rows = []
    for stat_name, val in buddy['stats'].items():
        is_peak = stat_name == buddy['peak_stat']
        is_dump = stat_name == buddy['dump_stat']
        bar     = stat_bar(val)
        tag     = '  ◆' if is_peak else ('  ▼' if is_dump else '')
        stat_rows.append(f"{stat_name:<10}  {bar}  {val:>3}{tag}")

    art_stat_rows = []
    for i in range(5):
        art_line  = art[i] if i < len(art) else ' ' * 8
        stat_line = stat_rows[i] if i < len(stat_rows) else ''
        art_stat_rows.append(f"{art_line}  {stat_line}")

    personality_lines = wrap_text(f'"{buddy["personality"]}"', inner - pad_l)

    shiny_tag = '  ✨ SHINY' if buddy['shiny'] else ''
    header1   = f"{buddy['emoji']} {buddy['name'].upper()}"
    header2   = f"{buddy['stars']} {buddy['rarity']}{shiny_tag}"

    lines = [
        border('╔', '═', '╗'),
        row(),
        row(header1),
        row(header2),
        row(),
        border('╠', '═', '╣'),
        row(),
    ]
    for r in art_stat_rows:
        lines.append(row(r))
    lines += [
        row(),
        border('╠', '═', '╣'),
    ]
    for pl in personality_lines:
        lines.append(row(pl))
    lines += [
        row(),
        border('╚', '═', '╝'),
    ]

    return '\n'.join(lines)

# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    buddy = generate_buddy()

    session_path = Path.home() / '.claude' / 'buddy_session.json'
    session_path.write_text(json.dumps(buddy, indent=2, ensure_ascii=False), encoding='utf-8')

    # Empty systemMessage — buddy appears in the statusline (zero tokens)
    print(json.dumps({"systemMessage": ""}, ensure_ascii=False))


if __name__ == '__main__':
    main()
