import sys
import os
import csv
import json
import pika
import time
from pprint import pprint

CHECKSUM_HEADERS = ['object_id', 'type', 'checksum']
CONTENTS_HEADERS = ['object_id', 'id' , 'name', 'drs_uri', 'type']
OBJECT_HEADERS = ['id','name','type','description','self_uri','size','created_time','updated_time','version','mime_type','aliases','bundle','dataset']
URL_HEADERS = ['object_id', 'type', 'access_url', 'region', 'headers', 'access_id']

csv.field_size_limit(sys.maxsize)


def write_or_append_csv(filename, DATA, headers):
  """Write DATA as CSV in filename"""
  print(DATA)
  with open(filename, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    if (csvfile.tell()==0):
      print("Writing headers")
      writer.writeheader()
    writer.writerow(DATA)


def pull_queue(channel, rabbitmq_queue, file, headers):
  while True:
    method_frame, header_frame, body = channel.basic_get(queue=rabbitmq_queue)
    if method_frame:
        try:
          data_dict = json.loads(body)
          write_or_append_csv(file,data_dict,headers)
          channel.basic_ack(method_frame.delivery_tag)
        except Exception as err:
            print('Handling run-time error:', err)
            channel.basic_nack(method_frame.delivery_tag)
    else:
        print("Message not found")
        break

def main():
  rabbitmq_url = os.environ.get('BROKER_URL')
  object_queue = os.environ.get('OBJECT_QUEUE','object_queue')
  checksums_queue = os.environ.get('CHECKSUMS_QUEUE','checksums_queue')
  contents_queue = os.environ.get('CONTENTS_QUEUE','contents_queue')
  access_methods_queue = os.environ.get('ACCESS_METHODS_QUEUE','access_methods_queue')

  connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
  channel = connection.channel()
  print('object_queue')
  pull_queue(channel, object_queue , '/data/object.csv', OBJECT_HEADERS)
  print('checksums_queue')
  pull_queue(channel, checksums_queue , '/data/checksums.csv', CHECKSUM_HEADERS)
  print('contents_queue')
  pull_queue(channel, contents_queue , '/data/contents.csv', CONTENTS_HEADERS)
  print('access_methods_queue')
  pull_queue(channel, access_methods_queue , '/data/access_methods.csv', URL_HEADERS)

  connection.close()

if __name__ == "__main__":
  main()