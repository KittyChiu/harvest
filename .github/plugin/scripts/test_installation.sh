#!/usr/bin/env bash
set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
temp_root="$(mktemp -d "${TMPDIR:-/tmp}/harvest-copilot.XXXXXX")"
snapshot_root="$temp_root/marketplace"
plugin_names="$temp_root/plugin-names"

cleanup() {
  rm -rf -- "$temp_root"
}
trap cleanup EXIT

export COPILOT_HOME="$temp_root/home"
export COPILOT_CACHE_HOME="$temp_root/cache"
mkdir -p "$COPILOT_HOME" "$COPILOT_CACHE_HOME"

python3 - "$repository_root" "$snapshot_root" "$plugin_names" <<'PY'
import json
import shutil
import sys
from pathlib import Path

source = Path(sys.argv[1])
snapshot = Path(sys.argv[2])
names_path = Path(sys.argv[3])
(snapshot / ".github" / "plugin").mkdir(parents=True)
shutil.copy2(
    source / ".github" / "plugin" / "marketplace.json",
    snapshot / ".github" / "plugin" / "marketplace.json",
)
shutil.copytree(
    source / "plugins",
    snapshot / "plugins",
    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
)
marketplace = json.loads(
    (snapshot / ".github" / "plugin" / "marketplace.json").read_text(
        encoding="utf-8"
    )
)
names_path.write_text(
    "".join(f"{entry['name']}\n" for entry in marketplace["plugins"]),
    encoding="utf-8",
)
PY

copilot plugin marketplace add "$snapshot_root"
browse_output="$(copilot plugin marketplace browse harvest)"

while IFS= read -r plugin; do
  grep -Fq "$plugin" <<<"$browse_output"
  copilot plugin install "$plugin@harvest"

  skill_root="$snapshot_root/plugins/$plugin/skills/$plugin"
  test -f "$snapshot_root/plugins/$plugin/plugin.json"
  test -f "$skill_root/SKILL.md"
  test -f "$skill_root/evals/evals.json"
  test -n "$(find "$skill_root/assets" -type f -print -quit)"
  test -n "$(find "$skill_root/references" -type f -print -quit)"
  test -n "$(find "$skill_root/scripts" -type f -name 'test_*.py' -print -quit)"
  while IFS= read -r validator; do
    python3 "$validator" --help >/dev/null
  done < <(find "$skill_root/scripts" -type f -name 'validate_*.py' | sort)
done <"$plugin_names"

list_output="$(copilot plugin list)"
grep -Fq "$snapshot_root" <<<"$list_output"
while IFS= read -r plugin; do
  grep -Fq "$plugin@harvest" <<<"$list_output"
done <"$plugin_names"

echo "Installed and validated every Harvest plugin from an isolated snapshot."
