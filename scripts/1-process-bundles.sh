#!/usr/bin/env bash
SCRIPT_PATH=${BASH_SOURCE[${#BASH_SOURCE[@]} - 1]}
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

DATASET_CSV=$1
DATASET_FILE="${DATASET_CSV##*/}"
DATASET_NAME="${DATASET_FILE%.*}"

# Exit if Bundles CSV is missing
if [ ! -f "$DATASET_CSV" ]; then
  echo "Missing CSV File: $DATASET_CSV"
  exit 1
fi

echo "Processing Dataset: $DATASET_NAME"

# Remove any existing .jobs or .missing files
[ -f "$DATASET_CSV.jobs" ] && rm "$DATASET_CSV.jobs"
[ -f "$DATASET_CSV.missing" ] && rm "$DATASET_CSV.missing"

sed 1d "$DATASET_CSV" | while IFS=, read -r dataset id pub_date dataset_url omicsdi_url omicsdi_api_url local_path
do
  # echo $dataset $id $pub_date $dataset_url $omicsdi_url $omicsdi_api_url $local_path
  local_path=$(echo "$local_path" | tr -d '\r')
  # Check if directory does not exist
  if [ ! -d "$local_path" ]; then
    echo "Missing Bundle $dataset:$id - $local_path"
    echo "$dataset $id $local_path" >> "$DATASET_CSV.missing"
  else
    echo "$dataset $id $local_path" >> "$DATASET_CSV.jobs"
  fi
done

# # Creating LSF Job Groups
echo "Creating LSF Job groups..."
bgadd "/$USER/$DATASET_NAME-list"
bgadd "/$USER/$DATASET_NAME-files"
bgadd "/$USER/$DATASET_NAME-dirs"
# bgadd "/$USER/$DATASET_NAME-errors"
bgadd "/$USER/$DATASET_NAME-extra"

NUM_JOBS=$(cat "$DATASET_CSV.jobs" | wc -l)
MAX_JOB_ARRAY_SIZE=$(bparams -l | grep MAX_JOB_ARRAY_SIZE | awk '{print $3}')
echo "NUM_JOBS: $NUM_JOBS MAX_JOB_ARRAY_SIZE: $MAX_JOB_ARRAY_SIZE"

if [ "$NUM_JOBS" -gt "$MAX_JOB_ARRAY_SIZE" ]; then
  JOB_SLICES=$(expr $NUM_JOBS / $MAX_JOB_ARRAY_SIZE)
  JOB_SLICES=$((JOB_SLICES+1))
  echo "JOB_SLICES: $JOB_SLICES"

  for i in $(seq 1 $JOB_SLICES); do
    END=$(expr $i \* $MAX_JOB_ARRAY_SIZE)
    START=$(expr $END - $MAX_JOB_ARRAY_SIZE + 1)
    if [ "$END" -gt "$NUM_JOBS" ]; then END=$NUM_JOBS; fi

    bsub -g /$USER/$DATASET_NAME-list -sp 100 -N -J filelist-${DATASET_NAME}-${i}[$START-$END] ${SCRIPT_DIR}/2-filelist.sh ${DATASET_CSV}.jobs

    bsub -g /$USER/$DATASET_NAME-files -sp 100 -w 'done(filelist-${DATASET_NAME}-${i}[*])' -N -J hashfiles-${DATASET_NAME}[$START-$END] ${SCRIPT_DIR}/3-hashfiles.sh ${DATASET_CSV}.jobs

    bsub -g /$USER/$DATASET_NAME-dirs -sp 100 -w 'done(hashfiles-${DATASET_NAME}-${i}[*])' -N -J hashdirs-${DATASET_NAME}[$START-$END] ${SCRIPT_DIR}/4-hashdirs.sh ${DATASET_CSV}.jobs

    bsub -g /$USER/$DATASET_NAME-errors -sp 100 -w 'done(hashdirs-${DATASET_NAME}-${i}[*])' -N -J find-errors ${SCRIPT_DIR}/5-find-errors.sh ${DATASET_NAME}

    bsub -g /$USER/$DATASET_NAME-extra -sp 100 -w 'done(hashdirs-${DATASET_NAME}-${i}[*])' -N -J hashextra-${DATASET_NAME}[$START-$END] ${SCRIPT_DIR}/6-hashextra.sh ${DATASET_CSV}.jobs

    bsub -g /$USER/$DATASET_NAME-extra -sp 100 -w 'done(hashdirs-${DATASET_NAME}-${i}[*])' -N -J hashpost-${DATASET_NAME}[$START-$END] ${SCRIPT_DIR}/7-post-process.sh ${DATASET_CSV}.jobs
  done
else
  echo "Submitting regular jobs"
  bsub -g "/$USER/$DATASET_NAME-list" -sp 100 -J "filelist-${DATASET_NAME}[1-${NUM_JOBS}]" "${SCRIPT_DIR}/2-filelist.sh" "${DATASET_CSV}.jobs"
  bsub -g "/$USER/$DATASET_NAME-files" -sp 100 -w "done(filelist-${DATASET_NAME}[*])" -J "hashfiles-${DATASET_NAME}[1-${NUM_JOBS}]" "${SCRIPT_DIR}/3-hashfiles.sh" "${DATASET_CSV}.jobs"
  bsub -g "/$USER/$DATASET_NAME-dirs" -sp 100 -w "done(hashfiles-${DATASET_NAME}[*])" -J "hashdirs-${DATASET_NAME}[1-${NUM_JOBS}]" "${SCRIPT_DIR}/4-hashdirs.sh" "${DATASET_CSV}.jobs"
  bsub -g "/$USER/$DATASET_NAME-errors" -sp 100 -w "done(hashdirs-${DATASET_NAME})" -J find-errors "${SCRIPT_DIR}/5-find-errors.sh" "${DATASET_NAME}"
  bsub -g "/$USER/$DATASET_NAME-extra" -sp 100 -w "done(hashdirs-${DATASET_NAME})" -J "hashextra-${DATASET_NAME}[1-$NUM_JOBS]" "${SCRIPT_DIR}/6-hashextra.sh" "${DATASET_CSV}.jobs"
  bsub -g "/$USER/$DATASET_NAME-extra" -sp 100 -w "done(hashdirs-${DATASET_NAME})" -J "hashpost-${DATASET_NAME}[1-$NUM_JOBS]" "${SCRIPT_DIR}/7-post-process.sh" "${DATASET_CSV}.jobs"
fi
