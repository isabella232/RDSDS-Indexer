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

echo "hashextra JobID: $JOB_ID Dataset: $DATASET Bundle: $BUNDLE"

DIR_LIST="${DATASET}/${BUNDLE}/${BUNDLE}.dirs"
FILE_LIST="${DATASET}/${BUNDLE}/${BUNDLE}.files"
BUNDLE_META="${DATASET}/${BUNDLE}/${BUNDLE}.meta"

sed -i '/hashextra timer_/d' "$BUNDLE_META"
TIMER_START=$SECONDS
echo "hashextra timer_start: $(date --iso-8601=seconds)" >> "$BUNDLE_META"

# Extra Processing
if [ "$DIRECTORY" == "" ]; then
  DIRECTORY=$(sort "$DIR_LIST" | awk '{for(i=4;i<=NF;++i)print $i}' | sort | head -1)
fi

# # IPFS
echo "Generating IPFS Hashes"
ipfs add -r --only-hash "$DIRECTORY" > "${DATASET}/${BUNDLE}/${BUNDLE}.ipfs"
ipfs=$(cat "${DATASET}/${BUNDLE}/${BUNDLE}.ipfs" | tail -1 | awk '{print $2}')
echo "hashextra ipfs: $ipfs" >> "$BUNDLE_META"
echo "hashextra ipfs_file: $(realpath ${DATASET}/${BUNDLE}/${BUNDLE}.ipfs)" >> "$BUNDLE_META"

# # Torrent
echo "Generating Torrent Hashes"
# torf "$DIRECTORY" -TWCSPDR -yo "${DATASET}/${BUNDLE}/${BUNDLE}.torrent"
rhash -r --bt-batch="${DATASET}/${BUNDLE}/${BUNDLE}.torrent" "$DIRECTORY"
btih=$(torf -i "${DATASET}/${BUNDLE}/${BUNDLE}.torrent" | grep "Info Hash" | awk '{print $3}')
magnet=$(torf -i "${DATASET}/${BUNDLE}/${BUNDLE}.torrent" | grep "Magnet" | awk '{print $2}')
echo "hashextra btih: $btih" >> "$BUNDLE_META"
echo "hashextra magnet: $magnet" >> "$BUNDLE_META"
echo "hashextra torrent_file: $(realpath ${DATASET}/${BUNDLE}/${BUNDLE}.torrent)" >> "$BUNDLE_META"


DURATION=$(( $SECONDS - $TIMER_START ))
echo "hashextra timer_end: $(date --iso-8601=seconds)" >> "$BUNDLE_META"
echo "hashextra timer_duration: $DURATION" >> "$BUNDLE_META"
