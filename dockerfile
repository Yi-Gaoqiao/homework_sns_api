FROM python:3.7-alpine
LABEL architecture="Yi Gaoqiao"

ENV PYTHONUNBUFFERD 1

COPY ./requirements.txt /requirements.txt
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers
RUN pip install -r /requirements.txt

RUN mkdir /sns-api
WORKDIR /sns-api
COPY ./sns-api /sns-api

RUN adduser -D user
USER user