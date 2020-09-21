#!/usr/bin/env bash
SCRIPT_PATH=${BASH_SOURCE[${#BASH_SOURCE[@]} - 1]}
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

echo "ARGS: $*"
DATASET=${1}

echo "#### START MISSING VALUES ####" > "$DATASET.csv.errors"
find "$DATASET" -type f -name "*.files.csv" -print0 | xargs -0 grep -l ",," >> "$DATASET.csv.errors"
echo "#### END MISSING VALUES ####" >> "$DATASET.csv.errors"

# cat "$DATASET.csv.errors" | grep ',,' | grep '^f'
# cat "$DATASET.csv.errors" | grep ',,' | grep '^d'

echo "#### START DIRS NOT PROCESSED ####" >> "$DATASET.csv.errors"
grep -L "^d"  "$DATASET"/*/*.files.csv >> "$DATASET.csv.errors"
echo "#### END DIRS NOT PROCESSED ####" >> "$DATASET.csv.errors"