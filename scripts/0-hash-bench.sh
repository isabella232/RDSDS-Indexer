#!/usr/bin/env bash
echo "Hostname: $(hostname)"
OUT_FILE="${1:-hash-bench.csv}"
realpath "$OUT_FILE"

# Create temporary files
TMP_DIR=$(mktemp -d)

cleanup() {
  rm -rf "$TMP_DIR"
}

trap cleanup SIGINT
trap cleanup SIGTERM

echo "Creating random files in: $TMP_DIR"
dd if=/dev/urandom of="$TMP_DIR/1K.dat" bs=1KB count=1 > /dev/null
dd if=/dev/urandom of="$TMP_DIR/10K.dat" bs=1KB count=10 > /dev/null
dd if=/dev/urandom of="$TMP_DIR/100K.dat" bs=1KB count=100 > /dev/null
dd if=/dev/urandom of="$TMP_DIR/1M.dat" bs=1M count=1 > /dev/null
dd if=/dev/urandom of="$TMP_DIR/10M.dat" bs=1M count=10 > /dev/null
dd if=/dev/urandom of="$TMP_DIR/100M.dat" bs=1M count=100 > /dev/null
dd if=/dev/urandom of="$TMP_DIR/1G.dat" bs=1M count=1024 > /dev/null
dd if=/dev/urandom of="$TMP_DIR/10G.dat" bs=1M count=10240 > /dev/null
# dd if=/dev/urandom of="$TMP_DIR/100G.dat" bs=1G count=102400 > /dev/null
wait

CRC32_BIN="cksum"
CRC32C_BIN="crc32c <"
MD5_BIN="MD5"
ETAG_BIN="s3md5 8"
SHA1_BIN="sha1sum"
SHA256_BIN="sha256sum"
SHA512_BIN="sha512sum"
BLAKE2B_BIN="b2sum"


TIMEFORMAT=%R
# echo "filename,md5sum,md5deep,sha1sum,sha1deep,sha256sum,sha256deep,xxhsum,blake2b,hashdeep" > "$OUT_FILE"
START=$SECONDS
echo "filename,crc32,crc32c,md5,etag,sha1,sha256,sha512,blake2b" > "$OUT_FILE.1"
for file in "$TMP_DIR"/*; do
  # Run each algo twice to warm up file cache
  t_crc32=$( (time $CRC32_BIN "$file" > /dev/null) 2>&1)
  t_crc32=$( (time $CRC32_BIN "$file" > /dev/null) 2>&1)

  t_crc32c=$( (time $CRC32C_BIN "$file" > /dev/null) 2>&1)
  t_crc32c=$( (time $CRC32C_BIN "$file" > /dev/null) 2>&1)

  t_md5=$( (time $MD5_BIN "$file" > /dev/null) 2>&1)
  t_md5=$( (time $MD5_BIN "$file" > /dev/null) 2>&1)

  t_etag=$( (time $ETAG_BIN "$file" > /dev/null) 2>&1)
  t_etag=$( (time $ETAG_BIN "$file" > /dev/null) 2>&1)

  t_sha1=$( (time $SHA1_BIN "$file" > /dev/null) 2>&1)
  t_sha1=$( (time $SHA1_BIN "$file" > /dev/null) 2>&1)

  t_sha256=$( (time $SHA256_BIN "$file" > /dev/null) 2>&1)
  t_sha256=$( (time $SHA256_BIN "$file" > /dev/null) 2>&1)

  t_sha512=$( (time $SHA512_BIN "$file" > /dev/null) 2>&1)
  t_sha512=$( (time $SHA512_BIN "$file" > /dev/null) 2>&1)

  t_blake2b=$( (time $BLAKE2B_BIN "$file" > /dev/null) 2>&1)
  t_blake2b=$( (time $BLAKE2B_BIN "$file" > /dev/null) 2>&1)

  echo "$(basename $file),$t_crc32,$t_crc32c,$t_md5,$t_etag,$t_sha1,$t_sha256,$t_sha512,$t_blake2b" >> "$OUT_FILE.1"
done

CRC32_BIN="rhash --crc32"
CRC32C_BIN="rhash --crc32c"
MD5_BIN="rhash --md5"
ETAG_BIN="s3md5 8"
SHA1_BIN="rhash --sha1"
SHA256_BIN="rhash --sha256"
SHA512_BIN="rhash --sha512"
BLAKE2B_BIN="b2sum"
RHASH_BIN="rhash --md5 --crc32 --crc32c --sha1 --sha256 --sha512 --bsd"

echo "filename,crc32,crc32c,md5,etag,sha1,sha256,sha512,blake2b" > "$OUT_FILE.2"
for file in "$TMP_DIR"/*; do
  # Run each algo twice to warm up file cache
  t_crc32=$( (time $CRC32_BIN "$file" > /dev/null) 2>&1)
  t_crc32=$( (time $CRC32_BIN "$file" > /dev/null) 2>&1)

  t_crc32c=$( (time $CRC32C_BIN "$file" > /dev/null) 2>&1)
  t_crc32c=$( (time $CRC32C_BIN "$file" > /dev/null) 2>&1)

  t_md5=$( (time $MD5_BIN "$file" > /dev/null) 2>&1)
  t_md5=$( (time $MD5_BIN "$file" > /dev/null) 2>&1)

  t_etag=$( (time $ETAG_BIN "$file" > /dev/null) 2>&1)
  t_etag=$( (time $ETAG_BIN "$file" > /dev/null) 2>&1)

  t_sha1=$( (time $SHA1_BIN "$file" > /dev/null) 2>&1)
  t_sha1=$( (time $SHA1_BIN "$file" > /dev/null) 2>&1)

  t_sha256=$( (time $SHA256_BIN "$file" > /dev/null) 2>&1)
  t_sha256=$( (time $SHA256_BIN "$file" > /dev/null) 2>&1)

  t_sha512=$( (time $SHA512_BIN "$file" > /dev/null) 2>&1)
  t_sha512=$( (time $SHA512_BIN "$file" > /dev/null) 2>&1)

  t_blake2b=$( (time $BLAKE2B_BIN "$file" > /dev/null) 2>&1)
  t_blake2b=$( (time $BLAKE2B_BIN "$file" > /dev/null) 2>&1)

  echo "$(basename $file),$t_crc32,$t_crc32c,$t_md5,$t_etag,$t_sha1,$t_sha256,$t_sha512,$t_blake2b" >> "$OUT_FILE.2"
done
echo "RHash Duration: $(( SECONDS - START ))"

START=$SECONDS
echo "filename,rhash,etag,blake2b" > "$OUT_FILE.3"
for file in "$TMP_DIR"/*; do
  # Run each algo twice to warm up file cache
  t_rhash=$( (time $RHASH_BIN "$file" > /dev/null) 2>&1)
  t_rhash=$( (time $RHASH_BIN "$file" > /dev/null) 2>&1)

  t_etag=$( (time $ETAG_BIN "$file" > /dev/null) 2>&1)
  t_etag=$( (time $ETAG_BIN "$file" > /dev/null) 2>&1)

  t_blake2b=$( (time $BLAKE2B_BIN "$file" > /dev/null) 2>&1)
  t_blake2b=$( (time $BLAKE2B_BIN "$file" > /dev/null) 2>&1)

  echo "$(basename $file),$t_rhash,$t_etag,$t_blake2b" >> "$OUT_FILE.3"
done
echo "RHash-Combined Duration: $(( SECONDS - START ))"

cleanup