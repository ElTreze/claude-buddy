# Claude Buddy 🐉

A session companion for Claude Code. Every time you open a new session, a random creature appears - with its own species, rarity, species-specific stats, and a personality phrase. Lives in your status bar the whole session, gone when you close it.

![Claude Buddy in action](screenshot.png)

## What you get

- **20 species** across 4 categories:
  - Animals: duck, goose, cat, rabbit, owl, penguin, turtle, snail, octopus, axolotl, capybara, fox
  - Mythical: dragon, ghost, phoenix
  - Plants: cactus, mushroom
  - Abstract: robot, blob, chonk
- **5 rarities**: Common (60%) · Uncommon (25%) · Rare (10%) · Epic (4%) · Legendary (1%)
- **✨ Shiny** variant: 1% chance
- **Species-specific stats**: each creature has its own 5 themed stats (duck gets QUACK/WADDLE/BREAD/POND_IQ/HONK, dragon gets FIRE/HOARD/RAVAGE/LORE/PRESENCE, etc.)
- **30 personality phrases** based on the creature's dominant stat archetype
- **Status bar** shows compact buddy info + personality phrase all session long - zero tokens burned
- **`/buddy`** skill to display or reroll mid-session

## Install

```bash
# 1. Clone into your Claude plugins folder
git clone https://github.com/ElTreze/claude-buddy ~/.claude/plugins/claude-buddy

# 2. Run the installer
# Windows:
python ~/.claude/plugins/claude-buddy/scripts/install.py

# Mac / Linux:
python3 ~/.claude/plugins/claude-buddy/scripts/install.py
```

Restart Claude Code after installing - your first buddy will appear in the status bar.

## Uninstall

```bash
python ~/.claude/plugins/claude-buddy/scripts/install.py --uninstall
```

## How it works

On session start, a Python script rolls your buddy (species, rarity, name, stats, personality) and saves it to `~/.claude/buddy_session.json`. The status line reads that file and shows a compact colored line throughout the session.

No network calls. No external dependencies. Pure Python stdlib.

## Status bar

```
🦊 Wumbo  ★★ UNCOMMON  TRI 87  "Does not read the docs. Does not need to. Usually."
```

Colors by rarity: white · green · cyan · magenta · gold

## Compatibility

- Requires Python 3.8+
- Works alongside any existing status line command (merges automatically)
- Tested on Windows 11 and macOS

## The card (via `/buddy`)

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  🦆 QUACKBERT                                        ║
║  ★★★ RARE                                           ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║   __       QUACK      ██████████   95  ◆            ║
║ <(oo)>     WADDLE     ██░░░░░░░░   18  ▼             ║
║   )(       BREAD      ████████░░   84                ║
║  /||\      POND_IQ    ██████░░░░   61                ║
║   ~~       HONK       █████████░   91                ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║  "Built different. Knows it."                        ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

## Species stats reference

| Species | Stat 1 | Stat 2 | Stat 3 | Stat 4 | Stat 5 |
|---------|--------|--------|--------|--------|--------|
| 🦆 duck | QUACK | WADDLE | BREAD | POND_IQ | HONK |
| 🪿 goose | HONK | GRUDGE | RAMPAGE | SPITE | MENACE |
| 🐱 cat | MURDER | IGNORE | ZOOM | DIGNITY | PURR |
| 🐰 rabbit | BINKY | FREEZE | ZAP | TWITCH | FLOOF |
| 🦉 owl | TALONS | VIGIL | SWIVEL | HOOT | MAJESTY |
| 🐧 penguin | SLIDE | HUDDLE | TOTTER | DIVE | TUXEDO |
| 🐢 turtle | SNAP | SHELL | DETOUR | ANCIENT | GENTLE |
| 🐌 snail | SLIME | CRAWL | SPIRAL | DEPTH | ANTENNA |
| 🐙 octopus | SQUEEZE | DRIFT | INK | BRAINS | CAMO |
| 🦎 axolotl | REGEN | FLOAT | WIGGLE | GILLS | CUTE |
| 🦫 capybara | CHOMP | ZEN | SPLASH | VIBE | FRIENDS |
| 🦊 fox | POUNCE | STALK | TRICK | CUNNING | SMUG |
| 🐉 dragon | FIRE | HOARD | RAVAGE | LORE | PRESENCE |
| 👻 ghost | PHASE | HAUNT | WAIL | MEMORY | SPOOK |
| 🔥 phoenix | BLAZE | REBIRTH | SURGE | ELDER | RADIANCE |
| 🌵 cactus | PRICKLE | DROUGHT | BLOOM | ROOT | SHADE |
| 🍄 mushroom | SPORES | DECAY | SPREAD | MYCEL | GLOW |
| 🤖 robot | COMPUTE | UPTIME | CRASH | LOGIC | SOCIAL |
| 🫧 blob | ABSORB | CHILL | SPLIT | VIBES | WOBBLE |
| 🐱 chonk | FLOP | NAP | ZOOMIE | LOAF | DEMAND |
