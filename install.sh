#!/usr/bin/env bash
# Claude Buddy - Mac/Linux installer
# Run: bash install.sh
# Uninstall: bash install.sh --uninstall

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$1" == "--uninstall" ]]; then
    python3 "$SCRIPT_DIR/scripts/install.py" --uninstall
else
    python3 "$SCRIPT_DIR/scripts/install.py"
fi
