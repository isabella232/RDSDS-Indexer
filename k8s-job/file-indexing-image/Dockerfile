# Specify BROKER_URL and QUEUE when running
FROM python:3.6

RUN apt update && \
    apt install -y gcc git make wget unzip lftp && \
    git clone https://github.com/rhash/RHash.git && \
    cd RHash/ && \
    ./configure --sysconfdir=/etc --exec-prefix=/usr --enable-lib-static && \
    make install install-lib-so-link install-lib-shared install-lib-headers && \
    wget https://bitbucket.org/dchest/b2sum/downloads/b2sum_linux_amd64.zip && \
    unzip b2sum_linux_amd64.zip && \
    cp b2sum /usr/bin/

COPY ./scripts ./scripts
COPY ./requirements.txt ./requirements.txt
COPY ./extract-files.py ./extract-files.py


RUN pip install -r ./requirements.txt && chmod +x ./extract-files.py && chmod -R +x ./scripts

CMD python ./extract-files.py