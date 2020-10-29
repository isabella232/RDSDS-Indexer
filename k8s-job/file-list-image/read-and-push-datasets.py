import sys
import os
import csv
import json
import pika
import requests
import boto3
from pprint import pprint
from botocore.exceptions import ClientError

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
    
def create_s3_client():
    session = boto3.session.Session()
    s3_client = session.client(
      service_name='s3',
      aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
      aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
      endpoint_url=os.environ.get('S3_ENDPOINT')
    )
    return s3_client

def download_file(file_name, bucket, s3_client, object_name):
  try:
      s3_client.download_file(bucket, object_name, file_name)
      print('File downloaded:' + object_name)
  except ClientError as e:
      print(e)
      raise e


def main():
  #csv_input = os.environ.get('CSV_INPUT')
  rabbitmq_url = os.environ.get('BROKER_URL')
  rabbitmq_queue = os.environ.get('QUEUE')

  #get_remote_csv(csv_input)

  s3_bucket = os.environ.get('S3_INPUT_BUCKET','rdsds-indexing')
  s3_filepath = os.environ.get('S3_INPUT_FILEPATH')
  s3_client = create_s3_client()
  download_file(csv_download_path,s3_bucket,s3_client,s3_filepath)

  data = read_csv(csv_download_path)

  print(data)

  connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
  channel = connection.channel()

  push_rabbitmq_jobs(data,channel,rabbitmq_queue)
  
  connection.close()

if __name__ == "__main__":
  main()