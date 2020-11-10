import sys
import csv
import argparse
import os
import parse
from settings import HASH_HEADERS, PATHS, HASH_TYPES

csv.field_size_limit(sys.maxsize)

CHECKSUM_HEADERS = ['object_id', 'type', 'checksum']

def read_csv(filename):
  """Read DATA from CSV in filename"""
  with open(filename) as f:
    reader = csv.DictReader(f)
    DATA = [r for r in reader]
    return DATA

def write_csv(filename, DATA, header=None):
  """Write DATA as CSV in filename"""
  with open(filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    writer.writerows(DATA)

def generate_checksums_each(dataset, bundle, data):
  checksums = []
  
  for hash in HASH_TYPES:
      checksum = {
          'object_id': data['id'],
          'type': hash,
          'checksum' : data[hash]
      }
      checksums.append(checksum)
      
  return checksums
  
def generate_checksums_all(dataset, bundle, filter, data):
  file_filter = filter.format(bundle + '/{}')
  bundle_filter = filter
  bundle_checksums = []
  for d in data:
    print(d['name'])
    if d['type'] == 'f':
      d['name'] = parse.parse(file_filter, d['name'])[0]
      checksums = generate_checksums_each(dataset, bundle, d)
      bundle_checksums.extend(checksums)
    else:
      d['name'] = parse.parse(bundle_filter, d['name'])[0]
      checksums = generate_checksums_each(dataset, bundle, d)
      bundle_checksums.extend(checksums)
  return bundle_checksums

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('dataset', help='Dataset')
  parser.add_argument('bundle', help='Bundle')
  parser.add_argument('filelist', help='File List CSV')
  args = parser.parse_args()

  data = read_csv(args.filelist)
  #filter = PATHS[args.dataset]['file'][0]
  #filter = '/mnt/c/Users/soumyadip/git/dsds-indexer/eva/{}'
  ftp_host = os.environ.get('FTP_URL', 'ftp.ebi.ac.uk')
  ftp_path = os.environ.get('FTP_PATH', '/pub/databases/')
  filter = '/data/' +  args.dataset + '/{}'
  bundle_checksums = generate_checksums_all(args.dataset, args.bundle, filter, data)
  out_filename = "{0}/{1}/{1}.checksums.csv".format(args.dataset, args.bundle)
  write_csv(out_filename, bundle_checksums, CHECKSUM_HEADERS)
  print("Checksums written to: {}".format(out_filename))

if __name__ == "__main__":
  main()