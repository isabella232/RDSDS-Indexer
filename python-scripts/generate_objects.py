import sys
import csv
import argparse
import parse
from settings import HASH_HEADERS, PATHS, HASH_TYPES
from pprint import pprint
from dateutil import parser as dateutil_parser

csv.field_size_limit(sys.maxsize)

OBJECT_HEADERS = ['id','name','type','description','self_uri','size','created_time','updated_time','version','mime_type','aliases','bundle','dataset']

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

def generate_objects_each(dataset, bundle, d):
    object_values = []
    print("Inserting {}..., {}...".format(d['id'][0:7], d['name'][0:10]))
    #print(d['timestamp'])
    timestamp = dateutil_parser.parse(d['timestamp'])
    object_values.append({
      'id': d['id'],
      'name': d['name'],
      'size': d['size'],
      'type': d['type'],
      'created_time': timestamp,
      'updated_time': timestamp,
      #'bundle': d['bundle'],
      #'dataset': d['dataset']
    })
      
    return object_values
  
def generate_objects_all(dataset, bundle, filter, data):
  file_filter = filter.format(bundle + '/{}')
  bundle_filter = filter
  bundle_objects = []
  for d in data:
    print(d['name'])
    d['name'] = parse.parse(bundle_filter, d['name'])[0]
    objects = generate_objects_each(dataset, bundle, d)
    bundle_objects.extend(objects)
  return bundle_objects

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('dataset', help='Dataset')
  parser.add_argument('bundle', help='Bundle')
  parser.add_argument('filelist', help='File List CSV')
  args = parser.parse_args()

  data = read_csv(args.filelist)
  filter = PATHS[args.dataset]['file'][0]
  #filter = '/mnt/c/Users/soumyadip/git/dsds-indexer/eva/{}'
  bundle_objects = generate_objects_all(args.dataset, args.bundle, filter, data)
  out_filename = "{0}/{1}/{1}.objects.csv".format(args.dataset, args.bundle)
  write_csv(out_filename, bundle_objects, OBJECT_HEADERS)
  print("objects written to: {}".format(out_filename))

if __name__ == "__main__":
  main()