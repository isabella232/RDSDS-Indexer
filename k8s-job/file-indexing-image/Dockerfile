# Specify BROKER_URL and QUEUE when running
FROM python:3.5

COPY ./local-scripts /local-scripts
COPY ./scripts /scripts

RUN pip install -r /requirements.txt && chmod +x /worker.py

CMD  ./scripts/extract-files.py