kubectl -n rdsds-indexing apply -f indexer-configmap.yml
kubectl -n rdsds-indexing delete -f job-file-listing.yml | kubectl -n rdsds-indexing create -f job-file-listing.yml
kubectl -n rdsds-indexing wait --for=condition=complete --timeout 1h -f job-file-listing.yml
kubectl -n rdsds-indexing delete -f job-file-indexing.yml | kubectl -n rdsds-indexing create -f job-file-indexing.yml
kubectl -n rdsds-indexing wait --for=condition=complete --timeout 24h -f job-file-indexing.yml
kubectl -n rdsds-indexing delete -f job-file-ingesting.yml | kubectl -n rdsds-indexing create -f job-file-ingesting.yml
kubectl -n rdsds-indexing wait --for=condition=complete --timeout 1h -f job-file-ingesting.yml

curl -X POST \
     -F token=${TRIGGER_TOKEN} \
     -F ref=wp-test-2 \
     -F variables[DB_MIGRATE]='sh scripts/migrate-csv-data.sh' \
     -F variables[K8S_SECRET_S3_HOST]='http://minio-1602831960.minio:9000' \
     -F variables[K8S_SECRET_S3_PATH]='s3://rdsds-indexing/indexed_items/' \
     -F variables[K8S_SECRET_AWS_ACCESS_KEY_ID]=${AWS_ACCESS_KEY} \
     -F variables[K8S_SECRET_AWS_SECRET_ACCESS_KEY]=${AWS_SECRET_KEY} \
     -F variables[K8S_SECRET_http_proxy]=${HTTP_PROXY} \
     -F variables[K8S_SECRET_https_proxy]=${HTTPS_PROXY} \
     -F variables[K8S_SECRET_HTTP_PROXY]=${HTTP_PROXY} \
     -F variables[K8S_SECRET_HTTPS_PROXY]=${HTTPS_PROXY} \
     -F variables[K8S_SECRET_NO_PROXY]='localhost,.cluster.local,.minio' \
     -F variables[K8S_SECRET_no_proxy]='localhost,.cluster.local,.minio' \
     ${TRIGGER_URL}