#!/usr/bin/env python3

import os
import sys
import argparse
import datetime
import textwrap
import requests
import json
import csv
import urllib
from pprint import pprint
from settings import OMICSDI, OMICSDI_HEADERS, PATHS


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
  for d in search_data['datasets']:
    did = d["id"]
    sub_dir = did.split('-')[1]
    pubDate = datetime.datetime.strptime(d["publicationDate"], '%Y%m%d')
    row = {
      'dataset': dataset,
      'id': did,
      'pub_date': datetime.datetime.strftime(pubDate, '%Y-%m-%d'),
      'dataset_url': OMICSDI[dataset]['dataset_url'].format(did),
      'omicsdi_url': OMICSDI[dataset]['omicsdi_url'].format(did),
      'omicsdi_api_url': OMICSDI[dataset]['omicsdi_api_url'].format(did),
      'local_path': PATHS[dataset]['file'][0].format("/".join([sub_dir, did]))
    }
    DATA.append(row)

def get_pride_datasets(dataset, search_data):
  """Custom extractor for PRIDE datasets"""
  # TODO: Extract external links from individual dataset json file_versions
  for d in search_data['datasets']:
    did = d["id"]
    pubDate = datetime.datetime.strptime(d["publicationDate"], '%Y%m%d')
    local_path_postfix = "/".join([str(pubDate.year), str(pubDate.month), did])
    row = {
      'dataset': dataset,
      'id': did,
      'pub_date': datetime.datetime.strftime(pubDate, '%Y-%m-%d'),
      'dataset_url': OMICSDI[dataset]['dataset_url'].format(did),
      'omicsdi_url': OMICSDI[dataset]['omicsdi_url'].format(did),
      'omicsdi_api_url': OMICSDI[dataset]['omicsdi_api_url'].format(did),
      'local_path': PATHS[dataset]['file'][0].format(local_path_postfix)
    }
    DATA.append(row)

def get_generic_datasets(dataset, search_data):
  """Generic extractor for datasets"""
  for d in search_data['datasets']:
    did = d["id"]
    pubDate = datetime.datetime.strptime(d["publicationDate"], '%Y%m%d')
    row = {
      'dataset': dataset,
      'id': did,
      'pub_date': datetime.datetime.strftime(pubDate, '%Y-%m-%d'),
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
    writer = csv.DictWriter(csvfile, fieldnames=OMICSDI_HEADERS)
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