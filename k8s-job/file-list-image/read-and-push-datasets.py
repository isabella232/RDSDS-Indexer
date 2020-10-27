import sys
import os
import csv
import json
import pika
import requests
from pprint import pprint

csv_download_path = '/tmp/input.csv'
csv.field_size_limit(sys.maxsize)

def get_remote_csv(url):
  r = requests.get(url, allow_redirects=True)
  open(csv_download_path, 'wb').write(r.content)

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

def push_rabbitmq_jobs(data, channel, rabbitmq_queue):
  for d in data:
    payload = json.dumps(d)
    channel.basic_publish(
    exchange='',
    routing_key=rabbitmq_queue,
    body=payload,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))
    print(" [x] Sent %r" % d)
    


def main():
  csv_input = os.environ.get('CSV_INPUT')
  rabbitmq_url = os.environ.get('BROKER_URL')
  rabbitmq_queue = os.environ.get('QUEUE')

  get_remote_csv(csv_input)
  data = read_csv(csv_download_path)

  connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
  channel = connection.channel()

  push_rabbitmq_jobs(data,channel,rabbitmq_queue)
  
  connection.close()

if __name__ == "__main__":
  main()