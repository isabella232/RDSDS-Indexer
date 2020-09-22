# Specify BROKER_URL and QUEUE when running
FROM python:3.5

COPY ./read-and-push-datasets.py /read-and-push-datasets.py
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt && chmod +x /worker.py

CMD  python /read-and-push-datasets.py 