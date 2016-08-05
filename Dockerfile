FROM python:2.7

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt && \
    python setup.py install && \
    python /app/docker/generate_production_ini.py

ENV ARTICLEMETA_SETTINGS_FILE=/app/production.ini
ENV PYTHONPATH=$PYTHONPATH:"/usr/local/lib/python2.7/site-packages/articles_meta":"/usr/local/lib/python2.7/site-packages/articles_meta/articlemeta/thrift"

EXPOSE 11620
EXPOSE 8000

ADD docker/docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
