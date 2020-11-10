# Specify BROKER_URL and QUEUE when running
FROM python:3.6

COPY ./read-and-push-datasets.py /read-and-push-datasets.py
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt  --use-feature=2020-resolver && chmod +x /read-and-push-datasets.py

CMD  python ./read-and-push-datasets.py 