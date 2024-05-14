FROM python:3.9-slim

RUN apt-get update -y

WORKDIR /front

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /front/requirements.txt

RUN pip install --upgrade -r /front/requirements.txt

COPY . /front/

