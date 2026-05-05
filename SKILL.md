---
name: buddy
description: Show your session's Claude Buddy — species, rarity, stats, and personality. Use /buddy to see your current companion or /buddy reroll to get a new one mid-session.
---

When this skill is invoked, read the file at `~/.claude/buddy_session.json` (Windows: `%USERPROFILE%/.claude/buddy_session.json`) using the Read tool.

If the file doesn't exist, tell the user the buddy hasn't been generated yet (they may need to restart Claude Code with the hook installed).

Display the buddy info in this exact format — no code fences, raw text:

1. Name, emoji, rarity stars, and ✨ SHINY tag if applicable
2. The ASCII art for the species side by side with the 5 species-specific stats
3. Stat bars (█ filled, ░ empty, 10 wide), value, and ◆ for peak stat / ▼ for dump stat
4. The personality phrase in quotes

If the user types `/buddy reroll`:
- Run `python ~/.claude/plugins/claude-buddy/scripts/generate_buddy.py` via Bash
- Then read the updated buddy_session.json and display the new buddy

If the user types `/buddy stats`:
- Show only the stats table without the full card

The buddy lives only for this session. Every new session brings a new companion.
