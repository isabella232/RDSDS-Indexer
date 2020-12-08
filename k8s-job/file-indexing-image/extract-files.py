import sys
import os
import csv
import json
import pika
import time
import subprocess
import requests

csv.field_size_limit(sys.maxsize)


def read_csv(filename):
  """Read DATA from CSV in filename"""
  with open(filename, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    DATA = [r for r in reader]
    return DATA

def get_file_url(dataset,bundle):
    ftp_host = os.environ.get('FTP_URL', 'ftp.ebi.ac.uk')
    ftp_path = os.environ.get('FTP_PATH', '/pub/databases/')
    ftp_url = 'ftp://' + ftp_host + ftp_path +  dataset + '/' + bundle + '/'
    return ftp_url

def get_local_dir(dataset,bundle):
    local_dir = '/data/' + dataset + '/' + bundle
    return local_dir

def get_files_from_omics_url(ftp_url,local_dir):
    subprocess.run(["mkdir", "-p" , local_dir])
    proxy = os.environ.get('HTTP_PROXY','')
    subprocess.run(["lftp", "-c" ,"set ftp:proxy "+ proxy +"; open " + ftp_url + "; set xfer:clobber on;  lcd " + local_dir + " ; mget *"], check=True)
    print ('file downloaded: ' + ftp_url)


def index_files(dataset, bundle , local_dir):
    subprocess.run(["./scripts/2-filelist-local.sh", dataset, bundle , local_dir ], check=True)
    subprocess.run(["./scripts/3-hashfiles-local.sh", dataset, bundle , local_dir ], check=True)
    subprocess.run(["./scripts/4-hashdirs-local.sh", dataset, bundle , local_dir ], check=True)
   # subprocess.run(["./scripts/6-hashextra-local.sh", dataset, bundle , local_dir ])
    subprocess.run(["./scripts/7-post-process-local.sh", dataset, bundle , local_dir ], check=True)
    print ('file indexed: ' + local_dir)

def write_indexes_to_queue(dataset,bundle,channel):
    csv_path = (dataset+ '/' + bundle)
    #cwd = subprocess.check_output(["echo", "${BASH_SOURCE[${#BASH_SOURCE[@]} - 1]}"])
    csv_path = ('/' + dataset+ '/' + bundle)
    subprocess.run(["ls", csv_path])
    object_data = read_csv(csv_path + '/'  + bundle + '.objects.csv')
    checksums_data = read_csv(csv_path + '/'  + bundle + '.checksums.csv')
    contents_data = read_csv(csv_path + '/'  + bundle + '.contents.csv')
    access_methods_data = read_csv(csv_path + '/'  + bundle + '.access_methods.csv')

    object_queue = os.environ.get('OBJECT_QUEUE','object_queue')
    checksums_queue = os.environ.get('CHECKSUMS_QUEUE','checksums_queue')
    contents_queue = os.environ.get('CONTENTS_QUEUE','contents_queue')
    access_methods_queue = os.environ.get('ACCESS_METHODS_QUEUE','access_methods_queue')

    push_rabbitmq_jobs(object_data, channel, object_queue)
    push_rabbitmq_jobs(checksums_data, channel, checksums_queue)
    push_rabbitmq_jobs(contents_data, channel, contents_queue)
    push_rabbitmq_jobs(access_methods_data, channel, access_methods_queue)
    
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

def cleanup_downloaded_files(local_dir):
    subprocess.run(["rm", "-r" , local_dir])

def main():
    rabbitmq_url = os.environ.get('BROKER_URL')
    rabbitmq_queue = os.environ.get('QUEUE')

    # extracting each dataset and indexing
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    while True:
        method_frame, header_frame, body = channel.basic_get(
            queue=rabbitmq_queue)
        if method_frame:
            try:
                omics_json = json.loads(body)
                print(omics_json)
                dataset = omics_json.get("dataset")
                bundle = omics_json.get("id")
                local_dir = get_local_dir(dataset,bundle)
                ftp_url=''
                if (omics_json.get("dataset_url")):
                  ftp_url = omics_json.get("dataset_url")
                else:
                  ftp_url = get_file_url(dataset,bundle)
                print('ftp_url:' + ftp_url)
                print('local_dir:' + local_dir)
                
                get_files_from_omics_url(ftp_url,local_dir)
                index_files(dataset, bundle, local_dir)
                write_indexes_to_queue(dataset,bundle,channel)
                print(' ### Message Processed: ' + bundle + '###' )

                channel.basic_ack(method_frame.delivery_tag)
                
                cleanup_downloaded_files(local_dir)
            except Exception as err:
                print('Handling run-time error:', err)
                channel.basic_nack(method_frame.delivery_tag)
                raise err
        else:
            print("Message not found")
            break
    connection.close()


if __name__ == "__main__":
    main()
