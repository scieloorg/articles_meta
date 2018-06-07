FROM python:3.5.2-alpine
ENV PYTHONUNBUFFERED 1

MAINTAINER tecnologia@scielo.org

COPY . /app
COPY production.ini-TEMPLATE /app/config.ini

WORKDIR /app

ENV ARTICLEMETA_SETTINGS_FILE=/app/config.ini

RUN apk add --no-cache --virtual .build-deps \
        make gcc libxml2-dev libxslt-dev git musl-dev \
    && apk add libxml2 libxslt \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir gunicorn \
    && python setup.py install \
    && apk --purge del .build-deps

