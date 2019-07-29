#!/usr/bin/env python3

import os
import sys
import argparse
import textwrap
import requests
import json
import csv
import urllib
from pprint import pprint
from settings import OMICSDI, PATHS

csv_column_names = ['dataset', 'id', 'dataset_url','omicsdi_url', 'omicsdi_api_url','local_path']
DATA = []

def request_url(URL):
  """Request URL and return JSON payload"""
  r = requests.get(URL)
  if r.status_code == requests.codes.ok:
    return json.loads(r.text)
  else:
    r.raise_for_status()

def get_arrayexpress_datasets(dataset, search_data):
  """Custom extractor for Arrayexpress datasets"""
  dataset_ids = [d['id'] for d in search_data['datasets']]
  for did in dataset_ids:
    sub_dir = did.split('-')[1]
    row = {
      'dataset': dataset,
      'id': did,
      'dataset_url': OMICSDI[dataset]['dataset_url'].format(did),
      'omicsdi_url': OMICSDI[dataset]['omicsdi_url'].format(did),
      'omicsdi_api_url': OMICSDI[dataset]['omicsdi_api_url'].format(did),
      'local_path': PATHS[dataset]['file'][0].format("/".join([sub_dir, did]))
    }
    DATA.append(row)

def get_pride_datasets(dataset, search_data):
  """Custom extractor for Pride datasets"""
  for d in search_data['datasets']:
    URL = OMICSDI[dataset]['omicsdi_api_url'].format(d['id'])
    print("Requesting: %s" % URL)
    r = request_url(URL)

    if 'file_versions' in r.keys():
      dataset_files = []
      for file_version in r['file_versions']:
        if file_version['type'] == 'primary':
          for _,v in file_version['files'].items():
            dataset_files.extend(v)
      dataset_prefix = os.path.commonprefix(dataset_files)
      archive_date_prefix = dataset_prefix.split("/"+d['id'])[0].split('pride/data/archive/')[-1]
      local_path_postfix = "/".join([archive_date_prefix, r['accession']])

      row = {
        'dataset': dataset,
        'id': r['accession'],
        'dataset_url': OMICSDI[dataset]['dataset_url'].format(r['accession']),
        'omicsdi_url': OMICSDI[dataset]['omicsdi_url'].format(r['accession']),
        'omicsdi_api_url': OMICSDI[dataset]['omicsdi_api_url'].format(r['accession']),
        'local_path': PATHS[dataset]['file'][0].format(local_path_postfix)
      }
      DATA.append(row)

def get_generic_datasets(dataset, search_data):
  """Generic extractor for datasets"""
  dataset_ids = [d['id'] for d in search_data['datasets']]
  for did in dataset_ids:
    row = {
      'dataset': dataset,
      'id': did,
      'dataset_url': OMICSDI[dataset]['dataset_url'].format(did),
      'omicsdi_url': OMICSDI[dataset]['omicsdi_url'].format(did),
      'omicsdi_api_url': OMICSDI[dataset]['omicsdi_api_url'].format(did),
      'local_path': PATHS[dataset]['file'][0].format(did)
    }
    DATA.append(row)

def get_datasets(dataset=None, start=0, size=100):
  """Request dataset pages from OMICSDI"""
  URL = OMICSDI['base_url']
  query = urllib.parse.quote_plus(OMICSDI[dataset]['query'])
  URL = URL + "&".join(["query=%s" % query, "start=%s" % start, "size=%s" % size])
  search_data = request_url(URL)
  count = search_data['count']
  percent_left = (start+100) / count
  print("Requested: {} ({:.2%} completed)".format(URL, percent_left))
  if dataset == "pride":
    get_pride_datasets(dataset, search_data)
  elif dataset == "arrayexpress":
    get_arrayexpress_datasets(dataset, search_data)
  else:
    get_generic_datasets(dataset, search_data)
  if count > start+100:
    get_datasets(dataset, start+100, size)

def export_csv(dataset, output):
  """Export dataset extract as CSV"""
  filename = '%s/%s.csv' % (output, dataset)
  with open(filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_column_names)
    writer.writeheader()
    writer.writerows(DATA)

def main():
  description = """\
    Scrape OmicsDI for dataset paths
    """
  parser = argparse.ArgumentParser(
        description=textwrap.dedent(description)
  )
  parser.add_argument('dataset', help='Dataset Repository')
  parser.add_argument('-o', '--output', default='data', help='Dataset Repository')
  args = parser.parse_args()

  if OMICSDI.get(args.dataset, None) is not None:
    get_datasets(args.dataset)
    export_csv(args.dataset, args.output)
  else:
    print("Error: Dataset metadata does not exist in settings.py")
    sys.exit(1)

if __name__ == "__main__":
  main()