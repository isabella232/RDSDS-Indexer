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


def pull_rabbitmq_job(ch, method, properties, body):
    print(" [x] %r" % body)
    

def main():
    rabbitmq_url = os.environ.get('BROKER_URL')
    rabbitmq_queue = os.environ.get('QUEUE')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_url))
    channel = connection.channel()
    channel.basic_consume(queue=rabbitmq_queue,
                          on_message_callback=pull_rabbitmq_job, auto_ack=True)
    connection.close()


if __name__ == "__main__":
    main()
