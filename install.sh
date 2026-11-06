#!/usr/bin/env bash
# Install or update the agent definitions in a target repository.
#
# Usage:
#   ./install.sh [--dry-run] [--yes] /path/to/target-repository
#
# See install.py for how updates and conflicts are handled.

set -euo pipefail

source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$source_dir/install.py" "$@"
