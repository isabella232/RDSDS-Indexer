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

echo "Processing Dataset: $DATASET_NAME $DATASET_FILE $DATASET_CSV"

# Remove any existing .jobs or .missing files
[ -f "$DATASET_CSV.jobs" ] && rm "$DATASET_CSV.jobs"
[ -f "$DATASET_CSV.missing" ] && rm "$DATASET_CSV.missing"


sed 1d "$DATASET_CSV" | while IFS=, read -r dataset id pub_date dataset_url omicsdi_url omicsdi_api_url local_path
do
  #echo $dataset $id $pub_date $dataset_url $omicsdi_url $omicsdi_api_url $local_path
  local_path=$(echo "$local_path" | tr -d '\r')
  echo "local_path:$local_path"
  # Check if directory does not exist
  if [ ! -d "$local_path" ]; then
    echo "Missing Bundle $dataset:$id - $local_path"
    echo "$dataset $id $local_path" >> "$DATASET_CSV.missing"
  else
          echo "$dataset $id $local_path" >> "$DATASET_CSV.jobs"
  fi
 
  echo "Arguments: $dataset $id $local_path"
  
  ${SCRIPT_DIR}/2-filelist-local.sh $dataset $id $local_path
  ${SCRIPT_DIR}/3-hashfiles-local.sh $dataset $id $local_path
  ${SCRIPT_DIR}/4-hashdirs-local.sh $dataset $id $local_path
  ${SCRIPT_DIR}/6-find-errors-local.sh $dataset $id $local_path
  #${SCRIPT_DIR}/6-hashextra-local.sh $dataset $id $local_path
  ${SCRIPT_DIR}/7-post-process-local.sh $dataset $id $local_path
done

