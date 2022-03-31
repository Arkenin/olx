FROM python:3.8-alpine

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /code
COPY *.py /code/
WORKDIR /code

CMD python main.py