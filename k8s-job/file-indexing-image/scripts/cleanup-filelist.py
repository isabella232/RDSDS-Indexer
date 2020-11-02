import sys
import csv
import argparse
import parse
import os
from settings import HASH_HEADERS, PATHS

csv.field_size_limit(sys.maxsize)

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

def cleanup_object_name(dataset, bundle, data):
  #filter = PATHS[args.dataset]['file'][0]
  #filter = '/mnt/c/Users/soumyadip/git/dsds-indexer/eva/{}'
  ftp_host = os.environ.get('FTP_URL', 'ftp.ebi.ac.uk')
  ftp_path = os.environ.get('FTP_PATH', '/pub/databases/')
  filter = '/data/' +  args.dataset + '/{}'
  file_filter = filter.format(bundle + '/{}')
  dir_filter = filter
  for d in data:
    if d['type'] == 'f':
      d['name'] = parse.parse(file_filter, d['name'])[0]
    else:
      d['name'] = parse.parse(dir_filter, d['name'])[0]
  return data

def cleanup(dataset, bundle, data):
  data = cleanup_object_name(dataset, bundle, data)
  return data

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('dataset', help='Dataset')
  parser.add_argument('bundle', help='Bundle')
  parser.add_argument('filelist', help='File List CSV')
  args = parser.parse_args()

  csv_data = read_csv(args.filelist)
  data = cleanup(args.dataset, args.bundle, csv_data)
  out_filename = args.filelist
  write_csv(out_filename, data, HASH_HEADERS)
  print("Cleaned Data written to: {}".format(out_filename))

if __name__ == "__main__":
  main()