import sys
import os
import csv
import json
import pika
import time
from pprint import pprint

count = 0
csv.field_size_limit(sys.maxsize)


def pull_rabbitmq_job(ch, method, properties, body):
   # print(" [x] %r" % body)
     #time.sleep(2.4)
     global count 
     count = count + 1
     print(count)
    

def main():
    rabbitmq_url = os.environ.get('BROKER_URL')
    rabbitmq_queue = os.environ.get('QUEUE')

    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    channel.basic_consume(queue=rabbitmq_queue,
                          on_message_callback=pull_rabbitmq_job, auto_ack=True)
    global count 
    print(count )
    channel.start_consuming()

    connection.close()


if __name__ == "__main__":
    main()
