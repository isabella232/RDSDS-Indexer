import sys
import os
import csv
import json
import pika
from pprint import pprint


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

def make_object_csv(channel,method_frame,body):
  try:
    file = '/data/object.csv'
    write_csv(file,body)
    channel.basic_ack(method_frame.delivery_tag)
  except Exception as err:
    print('Handling run-time error:', err)
    channel.basic_nack(method_frame.delivery_tag)
    
def make_contents_csv(channel,method_frame,body):
  try:
    file = '/data/contents.csv'
    write_csv(file,body)
    channel.basic_ack(method_frame.delivery_tag)
  except Exception as err:
    print('Handling run-time error:', err)
    channel.basic_nack(method_frame.delivery_tag)

def make_checksums_csv(channel,method_frame,body):
  try:
    file = '/data/checksums.csv'
    write_csv(file,body)
    channel.basic_ack(method_frame.delivery_tag)
  except Exception as err:
    print('Handling run-time error:', err)
    channel.basic_nack(method_frame.delivery_tag)

def make_access_methods_csv(channel,method_frame,body):
  try:
    file = '/data/access_methods.csv'
    write_csv(file,body)
    channel.basic_ack(method_frame.delivery_tag)
  except Exception as err:
    print('Handling run-time error:', err)
    channel.basic_nack(method_frame.delivery_tag)

def main():
  rabbitmq_url = os.environ.get('BROKER_URL')
  object_queue = os.environ.get('OBJECT_QUEUE','object_queue')
  checksums_queue = os.environ.get('CHECKSUMS_QUEUE','checksums_queue')
  contents_queue = os.environ.get('CONTENTS_QUEUE','contents_queue')
  access_methods_queue = os.environ.get('ACCESS_METHODS_QUEUE','access_methods_queue')

  connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
  channel = connection.channel()
  channel.basic_consume(queue=object_queue, on_message_callback=make_object_csv, auto_ack=False)
  channel.basic_consume(queue=checksums_queue, on_message_callback=make_checksums_csv, auto_ack=False)
  channel.basic_consume(queue=contents_queue, on_message_callback=make_contents_csv, auto_ack=False)
  channel.basic_consume(queue=access_methods_queue, on_message_callback=make_access_methods_csv, auto_ack=False)


  connection.close()

if __name__ == "__main__":
  main()