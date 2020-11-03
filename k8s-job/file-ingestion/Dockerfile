# Specify BROKER_URL and QUEUE when running
FROM python:3.9

COPY ./read-and-ingest-datasets.py /read-and-ingest-datasets.py
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt --use-feature=2020-resolver && chmod +x /read-and-ingest-datasets.py

CMD  python ./read-and-ingest-datasets.py 