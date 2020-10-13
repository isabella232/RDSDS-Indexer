# Specify BROKER_URL and QUEUE when running
FROM python:3.5

COPY ./scripts /scripts
COPY ./requirements.txt ./requirements.txt
COPY ./extract-files.py ./extract-files.py


RUN pip install -r ./requirements.txt && chmod +x ./extract-files.py

CMD  ./scripts/extract-files.py