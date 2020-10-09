import sys
import os
import csv
import json
import pika
import time
import subprocess
import requests

count = 0
csv.field_size_limit(sys.maxsize)


def pull_rabbitmq_job(ch, method, properties, body):
   # print(" [x] %r" % body)
     #time.sleep(2.4)
    global count 
    count = count + 1
    print(count)

def get_files_from_omics_url(omics_json):
    dataset = omics_json.get("dataset")
    id = omics_json.get("id")
    ftp_host = os.environ.get('FTP_URL', 'ftp.ebi.ac.uk')
    ftp_path = os.environ.get('FTP_PATH', '/pub/databases/')
    ftp_url = 'ftp://' + ftp_host + ftp_path +  dataset + '/' + id + '/*'
    print(ftp_url)
    local_dir = '/data/' + dataset + '/' + id
    print(local_dir)
    subprocess.call(["wget", "-r", "-q", "-P", "/data" ,ftp_url ])
    print ('file downloaded')
    #subprocess.call(["./2-filelist-local.sh", dataset, id , local_dir ])
    #subprocess.call(["./3-hashfiles-local.sh", dataset, id , local_dir ])
    #subprocess.call(["./4-hashdirs-local.sh", dataset, id , local_dir ])
    #subprocess.call(["./6-hashextra-local.sh", dataset, id , local_dir ])
    #subprocess.call(["./7-post-process-local.sh", dataset, id , local_dir ])



def main():
    rabbitmq_url = os.environ.get('BROKER_URL')
    rabbitmq_queue = os.environ.get('QUEUE')

    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    # channel.basic_consume(queue=rabbitmq_queue, on_message_callback=pull_rabbitmq_job, auto_ack=True)
    # channel.start_consuming()
    while True:
        method_frame, header_frame, body = channel.basic_get(
            queue=rabbitmq_queue)
        if method_frame:
            try:
                #print('body: ', body)
                omics_json = json.loads(body)
                #print(omics_json)
                get_files_from_omics_url(omics_json)
                time.sleep(2.4)
                channel.basic_ack(method_frame.delivery_tag)
            except Exception as err:
                print('Handling run-time error:', err)
                channel.basic_nack(method_frame.delivery_tag)
        else:
            print("Message not found")
            break
    connection.close()


if __name__ == "__main__":
    main()
