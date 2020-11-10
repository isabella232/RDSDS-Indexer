#!/usr/bin/env bash
SCRIPT_PATH=${BASH_SOURCE[${#BASH_SOURCE[@]} - 1]}
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
JOB_ID="${LSB_JOBINDEX:-0}"

if [ "$JOB_ID" -gt "0" ]; then
  echo "$(hostname) JOB ID: $JOB_ID"
  JOB_FILE="$1"
  ARGS=$(sed -n "${LSB_JOBINDEX}p" "$JOB_FILE")
  DATASET=$(echo "$ARGS" | awk '{print $1}')
  BUNDLE=$(echo "$ARGS" | awk '{print $2}')
  DIRECTORY=$(echo "$ARGS" | awk '{print $3}')
else
  echo "ARGS: $*"
  DATASET=${1}
  BUNDLE=${2}
  DIRECTORY=${3:-""}
fi

echo "post-process JobID: $JOB_ID Dataset: $DATASET Bundle: $BUNDLE"

DIR_LIST="${DATASET}/${BUNDLE}/${BUNDLE}.dirs"
FILE_LIST="${DATASET}/${BUNDLE}/${BUNDLE}.files"
BUNDLE_META="${DATASET}/${BUNDLE}/${BUNDLE}.meta"
FILE_LIST_CSV="${DATASET}/${BUNDLE}/${BUNDLE}.files.csv"

# Generate Access URLS
python3 "$SCRIPT_DIR/generate-access-urls.py" ${DATASET} ${BUNDLE} ${FILE_LIST_CSV}
python3 "$SCRIPT_DIR/generate_access_methods.py" ${DATASET} ${BUNDLE} ${FILE_LIST_CSV}
python3 "$SCRIPT_DIR/generate_checksums.py" ${DATASET} ${BUNDLE} ${FILE_LIST_CSV}
python3 "$SCRIPT_DIR/generate_contents.py" ${DATASET} ${BUNDLE} ${FILE_LIST_CSV}
python3 "$SCRIPT_DIR/generate_objects.py" ${DATASET} ${BUNDLE} ${FILE_LIST_CSV}
# Cleanup Filelist
python "$SCRIPT_DIR/cleanup-filelist.py" ${DATASET} ${BUNDLE} ${FILE_LIST_CSV}