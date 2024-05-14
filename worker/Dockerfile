FROM python:3.9-slim

RUN apt-get update -y

WORKDIR /worker

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /worker/requirements.txt

RUN pip install --upgrade -r /worker/requirements.txt
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /worker/

