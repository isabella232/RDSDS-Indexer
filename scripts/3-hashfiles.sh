#!/usr/bin/env bash
SCRIPT_PATH=${BASH_SOURCE[${#BASH_SOURCE[@]} - 1]}
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
JOB_ID="${LSB_JOBINDEX:-0}"
PATH=$HOME/.linuxbrew/bin:$PATH:$HOME/bin

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

echo "hashfiles JobID: $JOB_ID Dataset: $DATASET Bundle: $BUNDLE"

TIMEZONE=$(timedatectl | grep "Time zone:" | awk '{print $3}')
DIR_LIST="${DATASET}/${BUNDLE}/${BUNDLE}.dirs"
FILE_LIST="${DATASET}/${BUNDLE}/${BUNDLE}.files"
BUNDLE_META="${DATASET}/${BUNDLE}/${BUNDLE}.meta"
S3_DEFAULT_CHUNK_SIZE=8

sed -i '/hashfiles timer_/d' "$BUNDLE_META"
TIMER_START=$SECONDS
echo "hashfiles timer_start: $(date --iso-8601=seconds)" >> "$BUNDLE_META"

# echo "type,id,name,size,timestamp,crc32,crc32c,md5,etag,sha1,sha256,sha512,blake2b,contents" > "$FILE_LIST.csv"
echo "type,id,name,dataset,bundle,size,timestamp,crc32c,md5,sha256,sha512,trunc512,blake2b,contents" > "$FILE_LIST.csv"
while IFS=' ' read -r type size timestamp filename; do
  if [[ -r "$filename" ]]; then
    timestamp=$(python -c "import datetime; import pytz; tz = pytz.timezone('$TIMEZONE'); print(tz.localize(datetime.datetime.strptime('${timestamp%.*}', '%Y-%m-%d+%H:%M:%S')).isoformat())")
    echo "$filename, $size, $timestamp"
    md5=$(md5sum -b "$filename" | awk '{print $1}')
    # etag=$(s3md5 $S3_DEFAULT_CHUNK_SIZE "$filename") #DEPRECATED
    # crc32=$(cksum "$filename" | awk '{print $1}')
    crc32c=$(crc32c < "$filename")
    # sha1=$(sha1sum "$filename" | awk '{print $1}')
    sha256=$(sha256sum -b "$filename" | awk '{print $1}')
    sha512=$(sha512sum -b "$filename" | awk '{print $1}')
    trunc512=${sha512:0:48} #TRUNC512 = First 48 chars (24 bytes) of SHA512
    blake2b=$(b2sum "$filename" | awk '{print $1}')
    id="$blake2b"
    echo "$type,$id,§$filename§,$DATASET,$BUNDLE,$size,$timestamp,$crc32c,$md5,$sha256,$sha512,$trunc512,$blake2b,\"\"" >> "$FILE_LIST.csv"
  else
    echo "ERROR ReadPermission : $FILE_LIST.csv $filename"
    echo "ERROR ReadPermission : $FILE_LIST.csv $filename" >> "$DATASET.csv.errors"
    continue
  fi
done < "$FILE_LIST"

# Error Logs
meta_num_files=$(cat "${DATASET}/${BUNDLE}/${BUNDLE}.meta" | grep "num_files" | awk '{print $2}')
num_files=$(cat "$FILE_LIST.csv" | grep "^f" | wc -l)
if [ "$meta_num_files" -ne "$num_files" ]; then
  echo "ERROR FileCountMismatch : $FILE_LIST.csv" >> "$DATASET.csv.errors"
fi

DURATION=$(( $SECONDS - $TIMER_START ))
echo "hashfiles timer_end: $(date --iso-8601=seconds)" >> "$BUNDLE_META"
echo "hashfiles timer_duration: $DURATION" >> "$BUNDLE_META"