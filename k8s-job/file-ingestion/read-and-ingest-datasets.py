import sys
import os
import csv
import json
import pika
import boto3
from botocore.exceptions import ClientError

CHECKSUM_HEADERS = ['object_id', 'type', 'checksum']
CONTENTS_HEADERS = ['object_id', 'id' , 'name', 'drs_uri', 'type']
OBJECT_HEADERS = ['id','name','type','description','self_uri','size','created_time','updated_time','version','mime_type','aliases','bundle','dataset']
URL_HEADERS = ['object_id', 'type', 'access_url', 'region', 'headers', 'access_id']

csv.field_size_limit(sys.maxsize)


def write_or_append_csv(filename, DATA, headers):
  """Write DATA as CSV in filename"""
  print(DATA)
  with open(filename, mode='a', encoding='utf-8-sig') as csvfile:
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
            raise err
    else:
        print("Message not found")
        break

def create_s3_client():
    session = boto3.session.Session()
    s3_client = session.client(
      service_name='s3',
      aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
      aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
      endpoint_url=os.environ.get('S3_ENDPOINT')
    )
    return s3_client

def upload_file(file_name, bucket, s3_client, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param s3_client: boto3 s3 client
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        print(file_name)
        print(bucket)
        print(object_name)
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)
        raise e

def main():
  rabbitmq_url = os.environ.get('BROKER_URL')
  object_queue = os.environ.get('OBJECT_QUEUE','object_queue')
  checksums_queue = os.environ.get('CHECKSUMS_QUEUE','checksums_queue')
  contents_queue = os.environ.get('CONTENTS_QUEUE','contents_queue')
  access_methods_queue = os.environ.get('ACCESS_METHODS_QUEUE','access_methods_queue')

  # Pulling each queue and forming csv with records
  connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
  channel = connection.channel()
  pull_queue(channel, object_queue , '/data/object.csv', OBJECT_HEADERS)
  pull_queue(channel, checksums_queue , '/data/checksums.csv', CHECKSUM_HEADERS)
  pull_queue(channel, contents_queue , '/data/contents.csv', CONTENTS_HEADERS)
  pull_queue(channel, access_methods_queue , '/data/access_methods.csv', URL_HEADERS)
  connection.close()
  
  # Pushing to object store for ingestion
  s3_bucket = os.environ.get('S3_OUTPUT_BUCKET','rdsds-indexing')
  s3_filepath = os.environ.get('S3_OUTPUT_FILEPATH','indexed_items/')
  s3_client = create_s3_client()
  upload_file(file_name='/data/object.csv', bucket=s3_bucket, s3_client=s3_client,object_name=s3_filepath+'object.csv')
  upload_file(file_name='/data/checksums.csv', bucket=s3_bucket, s3_client=s3_client,object_name=s3_filepath+'checksums.csv')
  upload_file(file_name='/data/contents.csv', bucket=s3_bucket, s3_client=s3_client,object_name=s3_filepath+'contents.csv')
  upload_file(file_name='/data/access_methods.csv', bucket=s3_bucket, s3_client=s3_client,object_name=s3_filepath+'access_methods.csv')

  

if __name__ == "__main__":
  main()