import sys
import csv
import argparse
import parse
from settings import HASH_HEADERS, PATHS, HASH_TYPES
from pprint import pprint

csv.field_size_limit(sys.maxsize)

CONTENTS_HEADERS = ['object_id', 'id' ,'type', 'name']

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

def generate_contents(dataset, bundle, data):
  contents_values = []
  
  if data['contents']:
    object_conetnts = data['contents'].split(';')
    for oc in object_conetnts:
      if oc:
        split_oc = oc.split('::')
        contents_values.append({
          'object_id': data['id'],
          'id': split_oc[1],
          'type': split_oc[0],
          'name': split_oc[2]
        })
      
  return contents
  
def generate_contents(dataset, bundle, filter, data):
  file_filter = filter.format(bundle + '/{}')
  bundle_filter = filter
  bundle_contents = []
  for d in data:
    print(d['name'])
    if d['type'] != 'f':
      d['name'] = parse.parse(bundle_filter, d['name'])[0]
      contents = generate_contents(dataset, bundle, d)
      bundle_contents.extend(contents)
  return bundle_contents

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('dataset', help='Dataset')
  parser.add_argument('bundle', help='Bundle')
  parser.add_argument('filelist', help='File List CSV')
  args = parser.parse_args()

  data = read_csv(args.filelist)
  filter = PATHS[args.dataset]['file'][0]
  bundle_contents = generate_contents(args.dataset, args.bundle, filter, data)
  out_filename = "{0}/{1}/{1}.contents.csv".format(args.dataset, args.bundle)
  write_csv(out_filename, bundle_contents, CONTENTS_HEADERS)
  print("contents written to: {}".format(out_filename))

if __name__ == "__main__":
  main()