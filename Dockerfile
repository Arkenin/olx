FROM python:3.8-slim

RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    apt-get install -y locales locales-all && \
    locale-gen pl_PL.UTF-8

# Change to debian distro because of locale problems in alpine
# FROM python:3.8-alpine
# RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev
# RUN apk add libpq
# RUN apk del --no-cache .build-deps

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt


RUN mkdir -p /code
COPY *.py /code/
WORKDIR /code

CMD python main.py