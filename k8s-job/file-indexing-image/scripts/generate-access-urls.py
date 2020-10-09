import sys
import csv
import argparse
import parse
import os
from settings import HASH_HEADERS, PATHS, ACCESS_URLS
from pprint import pprint

csv.field_size_limit(sys.maxsize)

URL_HEADERS = ['object_id', 'type', 'access_url', 'region', 'headers', 'access_id']

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

def generate_url_paths(dataset, bundle, data):
  access_urls = []
  for path in ACCESS_URLS[dataset]:
    url = {
      'object_id': data['id'],
      'type': path['type'],
      'region': path['region'],
      'headers': path['headers'],
      'access_id': path['access_id']
    }
    if data['type'] == 'f':
      url['access_url'] = path['access_url'].format('/'.join([bundle, data['name']]))
    else:
      url['access_url'] = path['access_url'].format(data['name'])
    access_urls.append(url)
  return access_urls

def generate_access_urls(dataset, bundle, filter, data):
  file_filter = filter.format(bundle + '/{}')
  bundle_filter = filter
  access_urls = []
  for d in data:
    print(d)
    if d['type'] == 'f':
      d['name'] = parse.parse(file_filter, d['name'])[0]
      urls = generate_url_paths(dataset, bundle, d)
      access_urls.extend(urls)
    else:
      d['name'] = parse.parse(bundle_filter, d['name'])[0]
      urls = generate_url_paths(dataset, bundle, d)
      access_urls.extend(urls)
  return access_urls

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('dataset', help='Dataset')
  parser.add_argument('bundle', help='Bundle')
  parser.add_argument('filelist', help='File List CSV')
  args = parser.parse_args()

  data = read_csv(args.filelist)
  filter = PATHS[args.dataset]['file'][0]
  #filter = '/mnt/c/Users/soumyadip/git/dsds-indexer/eva/{}'
  #print(filter)
  ftp_host = os.environ.get('FTP_URL', 'ftp.ebi.ac.uk')
  ftp_path = os.environ.get('FTP_PATH', '/pub/databases/')
  filter = '/data/' + ftp_host + ftp_path +  args.dataset + '/{}'
  print('filter:' + filter)
  access_urls = generate_access_urls(args.dataset, args.bundle, filter, data)
  out_filename = "{0}/{1}/{1}.urls.csv".format(args.dataset, args.bundle)
  write_csv(out_filename, access_urls, URL_HEADERS)
  print("Access URLs written to: {}".format(out_filename))

if __name__ == "__main__":
  main()