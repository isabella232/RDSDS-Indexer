#!/usr/bin/env bash
SCRIPT_PATH=${BASH_SOURCE[${#BASH_SOURCE[@]} - 1]}
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
JOB_ID="${LSB_JOBINDEX:-0}"

if [ "$JOB_ID" -gt "0" ]; then
  echo "JOB_ID: $LSB_JOBINDEX"
  JOB_FILE="$1"
  ARGS=$(sed -n "${LSB_JOBINDEX}p" "$JOB_FILE")
  DATASET=$(echo "$ARGS" | awk '{print $1}')
  BUNDLE=$(echo "$ARGS" | awk '{print $2}')
  DIRECTORY=$(echo "$ARGS" | awk '{print $3}')
else
  echo "ARGS: $*"
  DATASET=${1}
  BUNDLE=${2}
  DIRECTORY=${3}
fi

echo "$JOB_ID $DATASET $BUNDLE $DIRECTORY"

mkdir -p "$DATASET/$BUNDLE" && cd "$DATASET/$BUNDLE"

# find ERZ1175{85..95} -printf '%Y %s %T+ %p\n'
find ${DIRECTORY} -printf '%Y %s %T+ %p\n' > "$BUNDLE.tree"

cat "$BUNDLE.tree" | grep "^d" > "$BUNDLE.dirs"
[ ! -s "$BUNDLE.dirs" ] && rm "$BUNDLE.dirs"
# cat "$BUNDLE.tree" | grep "^d" | awk '{print $2}' > "$BUNDLE.dirs"
# find ${DIRECTORY} -type d -print > "$BUNDLE.dirs"

cat "$BUNDLE.tree" | grep "^f" > "$BUNDLE.files"
[ ! -s "$BUNDLE.files" ] && rm "$BUNDLE.files"
# cat "$BUNDLE.tree" | grep "^f" | awk '{print $2}' > "$BUNDLE.files"
# find ${DIRECTORY} -type f -print > "$BUNDLE.files"

cat "$BUNDLE.tree" | grep "^l" > "$BUNDLE.links"
[ ! -s "$BUNDLE.links" ] && rm "$BUNDLE.links"
# cat "$BUNDLE.tree" | grep "^l" | awk '{print $2}' > "$BUNDLE.links"
# find ${DIRECTORY} -type l -print > "$BUNDLE.links"

echo "name: $BUNDLE" > "$BUNDLE.meta"
echo "directory: ${DIRECTORY}" >> "$BUNDLE.meta"
echo "total_size_bytes: $(du -s -B1 $DIRECTORY | awk '{print $1}')" >> "$BUNDLE.meta"
echo "timestamp: $(date --iso-8601=seconds)" >> "$BUNDLE.meta"
echo "tree_file: $(realpath $BUNDLE.tree)" >> "$BUNDLE.meta"
echo "num_tree: $(cat $BUNDLE.tree | wc -l)" >> "$BUNDLE.meta"
echo "dirs_file: $(realpath $BUNDLE.dirs)" >> "$BUNDLE.meta"
echo "num_dirs: $(cat $BUNDLE.dirs | wc -l)" >> "$BUNDLE.meta"
echo "files_file: $(realpath $BUNDLE.files)" >> "$BUNDLE.meta"
echo "num_files: $(cat $BUNDLE.files | wc -l)" >> "$BUNDLE.meta"
echo "links_file: $(realpath $BUNDLE.links)" >> "$BUNDLE.meta"
echo "num_links: $(cat $BUNDLE.links | wc -l)" >> "$BUNDLE.meta"

cat "$BUNDLE.meta"

# Find newer files in root bundle
# find "${DIRECTORY}" -newer "{BUNDLE}.files.csv" -printf '%Y %s %T+ %p\n'
# find ${DIRECTORY} -newermt "2019-01-01 00:00:00" -printf '%Y %s %T+ %p\n'