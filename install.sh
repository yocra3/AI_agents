#!/usr/bin/env bash
# Copy the agent definitions into a target repository.
#
# Usage:
#   ./install.sh /path/to/target-repository

set -euo pipefail

if [[ $# -ne 1 || ! -d $1 ]]; then
    echo "Usage: $0 /path/to/target-repository" >&2
    exit 1
fi

source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target_dir="$(cd "$1" && pwd)"

for folder in .agents .claude .codex; do
    if [[ -e $target_dir/$folder ]]; then
        echo "install: $target_dir/$folder already exists; remove it or merge it manually" >&2
        exit 1
    fi
done

# cp -a keeps the .claude/skills -> ../.agents/skills symbolic link
cp -a "$source_dir/.agents" "$source_dir/.claude" "$source_dir/.codex" "$target_dir/"

python3 "$target_dir/.claude/scripts/generate_agents.py" "$target_dir"

echo "Installed. Next: generate AGENTS.md with the project-bootstrap skill and add a CLAUDE.md (see README.md)."
