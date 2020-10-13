# Specify BROKER_URL and QUEUE when running
FROM python:3.5

COPY ./scripts /scripts
COPY ./requirements.txt ./requirements.txt
COPY ./worker.py ./worker.py


RUN pip install -r ./requirements.txt && chmod +x ./worker.py

CMD  ./scripts/extract-files.py