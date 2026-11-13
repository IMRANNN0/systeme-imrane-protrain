#!/bin/sh
# macOS: sh bootstrap.sh /absolute/workspace [core|complete] [--apply]
set -eu
workspace=${1:?Pass a workspace path}
profile=${2:-complete}
apply=${3:-}
case "$profile" in core|complete) ;; *) echo 'Unknown profile' >&2; exit 2;; esac
case "$apply" in ''|--apply) ;; *) echo 'Use --apply or omit it for a plan' >&2; exit 2;; esac
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=''
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)' 2>/dev/null; then
    python_bin=$candidate
    break
  fi
done
if [ -z "$python_bin" ]; then
  echo 'Missing Python >=3.11. Plan: brew install python@3.12'
  if [ "$apply" = '--apply' ]; then
    command -v brew >/dev/null 2>&1 || { echo 'Install Homebrew from https://brew.sh, then rerun.' >&2; exit 1; }
    brew install python@3.12
    echo 'Open a new terminal, ensure Python 3.12 is on PATH, then rerun.'
  fi
  exit 1
fi
if [ "$apply" = '--apply' ]; then
  "$python_bin" "$script_dir/scripts/imrane.py" deps --workspace "$workspace" --profile "$profile" --apply
  "$python_bin" "$script_dir/scripts/imrane.py" init --workspace "$workspace" --apply
  if [ "$profile" = 'complete' ]; then
    "$python_bin" "$script_dir/scripts/skills.py" install --workspace "$workspace" --all --apply
  else
    echo 'Core profile: no optional skills installed; use complete or install chosen GitHub skills individually.'
  fi
else
  "$python_bin" "$script_dir/scripts/imrane.py" deps --workspace "$workspace" --profile "$profile"
  "$python_bin" "$script_dir/scripts/imrane.py" init --workspace "$workspace"
  if [ "$profile" = 'complete' ]; then
    "$python_bin" "$script_dir/scripts/skills.py" install --workspace "$workspace" --all
  fi
fi
