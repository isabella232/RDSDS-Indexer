import sys
import os
import csv
import json
import pika
import time
from pprint import pprint

csv.field_size_limit(sys.maxsize)

def pull_rabbitmq_job(ch, method, properties, body):
  print(" [x] %r" % body)
  ch.basic_nack(method.delivery_tag)

def main():
  rabbitmq_url = os.environ.get('BROKER_URL')

  connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
  channel = connection.channel()
  channel.basic_consume(queue='job2', on_message_callback=pull_rabbitmq_job, auto_ack=False)
  channel.start_consuming()
  connection.close()

if __name__ == "__main__":
  main()