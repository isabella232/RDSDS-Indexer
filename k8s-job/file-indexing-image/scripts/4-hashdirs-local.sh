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

echo "hashdirs JobID: $JOB_ID Dataset: $DATASET Bundle: $BUNDLE"

#TIMEZONE=$(timedatectl | grep "Time zone:" | awk '{print $3}')
TIMEZONE='Europe/London'
DIR_LIST="${DATASET}/${BUNDLE}/${BUNDLE}.dirs"
FILE_LIST="${DATASET}/${BUNDLE}/${BUNDLE}.files"
BUNDLE_META="${DATASET}/${BUNDLE}/${BUNDLE}.meta"
S3_DEFAULT_CHUNK_SIZE=8

# if grep -Fxq "$FILENAME" "$DATASET.csv.errors"; then
#   echo "ERROR ExistingErrors : $FILE_LIST.csv" >> "$DATASET.csv.errors"
# fi

cleanup() {
  while IFS=' ' read -r tmp_dir ftp_dir
  do
    if [[ $tmp_dir =~ ^/tmp/tmp.* ]]; then
      rm -rf $tmp_dir
    fi
  done < "${FILE_LIST}.csv.tmpdirs"
}
touch "${FILE_LIST}.csv.tmpdirs"
trap cleanup EXIT
trap cleanup SIGINT
trap cleanup SIGTERM

sed -i '/hashdirs timer_/d' "$BUNDLE_META"
TIMER_START=$SECONDS
echo "hashdirs timer_start: $(date --iso-8601=seconds)" >> "$BUNDLE_META"

# Extracting Directory Timestamps
echo "Start: Collecting directory names & timestamps"
DIR_NAMES=()
declare -A DIR_TIMESTAMPS
while IFS=' ' read -r type size timestamp name; do
  name=${name%/}
  DIR_NAMES+=("$name")
  timestamp=${timestamp%.*}
  timestamp=$(python -c "import datetime; import pytz; tz = pytz.timezone('$TIMEZONE'); print(tz.localize(datetime.datetime.strptime('${timestamp}', '%Y-%m-%d+%H:%M:%S')).isoformat())")
  DIR_TIMESTAMPS[$name]=$timestamp
done < "$DIR_LIST"
echo "Finished: Collecting directory names & timestamps"

echo "Start: Collecting sub-directory files to hash"
touch "${FILE_LIST}.csv.tmpdirs"
IFS=$'\n' DIR_NAMES=($(sort -r <<<"${DIR_NAMES[*]}"))
for dir in "${DIR_NAMES[@]}"; do
  if [ "$(ls -A $dir)" ]; then  # If not empty
    TMP_DIR=$(mktemp -d)
    echo "$HOSTNAME $TMP_DIR $dir" | tee -a "${FILE_LIST}.csv.tmpdirs"
    find "$dir" -maxdepth 1 -print0 | while IFS= read -r -d '' object; do
      echo "Object: $object"
      line=$(grep "§$object§" "${FILE_LIST}.csv")
      filename=$object
      dirname=$(dirname "$object")
      echo "Line: $line"
      echo "Filename: $filename Dirname: $dirname"
      # Skip if object already in list of errors
      if grep -Fxq "$object" "$DATASET.csv.errors"; then
        echo "Skipping as object already in list of errors"
        continue
      fi
      # Calculate cumulative hashes and sizes
      if [ "$dirname" == "$dir" ]; then
        echo "DirEq Line: $line"
        type=$(echo "$line" | tr ',' '\n' | sed -n 1p)
        id=$(echo "$line" | tr ',' '\n' | sed -n 2p)
        echo "$id $filename $type" >> "$TMP_DIR/ids+names"
        echo "$line" | tr ',' '\n' | sed -n 6p >> "$TMP_DIR/sizes"
        echo "$line" | tr ',' '\n' | sed -n 8p >> "$TMP_DIR/crc32c"
        echo "$line" | tr ',' '\n' | sed -n 9p >> "$TMP_DIR/md5"
        echo "$line" | tr ',' '\n' | sed -n 10p >> "$TMP_DIR/sha256"
        echo "$line" | tr ',' '\n' | sed -n 11p >> "$TMP_DIR/sha512"
        echo "$line" | tr ',' '\n' | sed -n 13p >> "$TMP_DIR/blake2b"
      fi
    done
    # Sort ids and corresponding names
    sort "$TMP_DIR/ids+names" | while IFS=' ' read -r id name type; do
      echo "$id" >> "$TMP_DIR/ids"
      name="${name#$DIRECTORY/}"
      name=${name%/}
      echo "$type::$id::$name" >> "$TMP_DIR/ids+names.sorted"
    done

    id=$(cat "$TMP_DIR/ids" | tr -d ' ' | tr -d '\n's | b2sum | awk '{print $1}')
    names=$(cat "$TMP_DIR/ids+names.sorted" | tr '\n' ';')
    timestamp="${DIR_TIMESTAMPS[$dir]}"
    size=$(awk '{s+=$1} END {printf "%.0f", s}' "$TMP_DIR/sizes")

    md5=$(sort "$TMP_DIR/md5" | tr -d ' '| tr -d '\n' | rhash --md5 | awk '{print $1}')
    # crc32=$(sort "$TMP_DIR/crc32" | tr -d ' '| tr -d '\n' | cksum | awk '{print $1}')

    sort "$TMP_DIR/crc32c" | tr -d ' '| tr -d '\n' >> "$TMP_DIR/crc32c.bin"
    crc32c=$(rhash --crc32c "$TMP_DIR/crc32c.bin" | awk '{print $1}')

    # sort "$TMP_DIR/etag" | tr -d ' '| tr -d '\n' >> "$TMP_DIR/etag.bin"
    # etag=$(s3md5 $S3_DEFAULT_CHUNK_SIZE "$TMP_DIR/etag.bin" | awk '{print $1}')

    # sha1=$(sort "$TMP_DIR/sha1" | tr -d ' '| tr -d '\n' | sha1sum | awk '{print $1}')
    sha256=$(sort "$TMP_DIR/sha256" | tr -d ' '| tr -d '\n' | rhash --sha256 | awk '{print $1}')
    sha512=$(sort "$TMP_DIR/sha512" | tr -d ' '| tr -d '\n' | rhash --sha512 | awk '{print $1}')
    trunc512=$(sort "$TMP_DIR/sha512" | cut -c -48 | tr -d ' '| tr -d '\n' | sha512sum -b | awk '{print $1}' | cut -c -48)
    blake2b=$(sort "$TMP_DIR/blake2b" | tr -d ' '| tr -d '\n' | b2sum | awk '{print $1}')
    echo "d,$id,§$dir§,$DATASET,$BUNDLE,$size,$timestamp,$crc32c,$md5,$sha256,$sha512,$trunc512,$blake2b,\"$names\"" >> "$FILE_LIST.csv"
  else
    echo "$dir Empty"
  fi
done
echo "Finished: Collecting sub-directory files to hash"

# Convert §§ to ""
sed "s/§/\"/g" "$FILE_LIST.csv" > "$FILE_LIST.csv.tmp"
mv "$FILE_LIST.csv.tmp" "$FILE_LIST.csv"

# Error Logs
meta_num_dirs=$(cat "${DATASET}/${BUNDLE}/${BUNDLE}.meta" | grep num_dirs | awk '{print $2}')
num_dirs=$(cat "$FILE_LIST.csv" | grep "^d" | wc -l)
if [ "$meta_num_dirs" -ne "$num_dirs" ]; then
  echo "ERROR DirCountMismatch : $FILE_LIST.csv" >> "$DATASET.csv.errors"
fi


DURATION=$(( $SECONDS - $TIMER_START ))
echo "hashdirs timer_end: $(date --iso-8601=seconds)" >> "$BUNDLE_META"
echo "hashdirs timer_duration: $DURATION" >> "$BUNDLE_META"