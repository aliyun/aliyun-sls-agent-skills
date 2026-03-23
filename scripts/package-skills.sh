#!/usr/bin/env bash
set -euo pipefail

SKILLS_DIR=".agents/skills"
OUTPUT_DIR="${1:-dist/skills}"

if [ ! -d "$SKILLS_DIR" ]; then
  echo "Error: Skills directory '$SKILLS_DIR' not found." >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

skill_count=0

for skill_path in "$SKILLS_DIR"/*/; do
  [ -d "$skill_path" ] || continue

  skill_name=$(basename "$skill_path")
  zip_file="$OUTPUT_DIR/${skill_name}.zip"

  echo "Packaging skill: $skill_name -> $zip_file"
  (cd "$skill_path" && zip -r - .) > "$zip_file"

  skill_count=$((skill_count + 1))
done

if [ "$skill_count" -eq 0 ]; then
  echo "Warning: No skills found in '$SKILLS_DIR'." >&2
  exit 1
fi

echo "Done. Packaged $skill_count skill(s) into '$OUTPUT_DIR'."
