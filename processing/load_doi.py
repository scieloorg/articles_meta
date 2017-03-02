# coding: utf-8
"""
This scripts scrapy the DOI of the scielo documents from the website
and load them into the Articlemeta, this process is necessary because the
legacy databases does not have the doi persisted for each document.
"""
import logging
import logging.config
import re
import os
import argparse
from datetime import datetime, timedelta
import requests
from lxml import etree
from io import BytesIO
from pymongo import MongoClient
from xylose.scielodocument import Article
from articlemeta import utils

logger = logging.getLogger(__name__)
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
MONGODB_HOST = os.environ.get('MONGODB_HOST', None)

DOI_REGEX = re.compile(r'[0-9][0-9]\.[0-9].*/.*\S')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'console': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%H:%M:%S',
            },
        },
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'console'
            }
        },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': LOGGING_LEVEL,
            'propagate': False,
            },
        'processing.load_doi': {
            'level': LOGGING_LEVEL,
            'propagate': True,
        },
    }
}

if SENTRY_DSN:
    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'raven.handlers.logging.SentryHandler',
        'dsn': SENTRY_DSN,
    }
    LOGGING['loggers']['']['handlers'].append('sentry')


FROM = datetime.now() - timedelta(days=15)
FROM = FROM.isoformat()[:10]

try:
    articlemeta_db = MongoClient(MONGODB_HOST)['articlemeta']
except:
    logging.error('Fail to connect to (%s)', settings['app:main']['mongo_uri'])


def collections_acronym():

    collections = articlemeta_db['collections'].find({}, {'_id': 0})

    return [i['code'] for i in collections]


def collection_info(collection):

    info = articlemeta_db['collections'].find_one({'acron': collection}, {'_id': 0})

    return info


def load_documents(collection, all_records=False):

    fltr = {
        'collection': collection
    }

    if all_records == False:
        fltr['doi'] = {'$exists': 0}

    documents = articlemeta_db['articles'].find(
        fltr,
        {'_id': 0, 'citations': 0},
        no_cursor_timeout=True
    )

    for document in documents:
        yield Article(document)

    documents.close()


def do_request(url, json=True):

    headers = {
        'User-Agent': 'SciELO Processing ArticleMeta: LoadDoi'
    }

    try:
        document = requests.get(url, headers=headers)
    except:
        logger.error(u'HTTP request error for: %s', url)
    else:
        if json:
            return document.json()
        else:
            return document.text


def scrap_doi(data):

    data = ' '.join([i.strip() for i in data.split('\n')])

    parser = etree.HTMLParser(remove_blank_text=True, encoding='utf-8')
    tree = etree.parse(BytesIO(data.encode('utf-8')), parser)

    etree_doi = tree.find('.//meta[@name="citation_doi"]')

    if etree_doi is None:
        logger.debug('DOI not found')
        return None

    result = DOI_REGEX.findall(etree_doi.get('content'))

    if not result:
        logger.debug('DOI not found')
        return None

    return result


def run(collections, all_records=False):

    if not isinstance(collections, list):
        logger.error('Collections must be a list o collection acronym')
        exit()

    for collection in collections:
        coll_info = collection_info(collection)

        logger.info(u'Loading DOI for %s', coll_info['domain'])
        logger.info(u'Using mode all_records %s', str(all_records))

        for document in load_documents(collection, all_records=all_records):

            doi = None
            try:
                data = do_request(document.html_url(), json=False)
            except:
                logger.error('Fail to load url: %s', document.html_url())
                continue

            try:
                doi = scrap_doi(data)
            except:
                logger.error('Fail to scrap: %s', document.publisher_id)
                continue

            if not doi:
                logger.debug('No DOI defined for: %s', document.publisher_id)
                continue

            articlemeta_db['articles'].update(
                {'code': document.publisher_id, 'collection': document.collection_acronym},
                {'$set': {'doi': doi}}
            )

            logger.debug('DOI Found %s: %s', document.publisher_id, doi)


def main():
    parser = argparse.ArgumentParser(
        description="Load documents DOI from SciELO website"
    )

    parser.add_argument(
        '--collection',
        '-c',
        choices=collections_acronym(),
        help='Collection acronym'
    )

    parser.add_argument(
        '--all_records',
        '-a',
        action='store_true',
        help='Apply processing to all records or just records without the license parameter'
    )

    parser.add_argument(
        '--logging_level',
        '-l',
        default=LOGGING_LEVEL,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logggin level'
    )

    args = parser.parse_args()
    LOGGING['handlers']['console']['level'] = args.logging_level
    for lg, content in LOGGING['loggers'].items():
        content['level'] = args.logging_level

    logging.config.dictConfig(LOGGING)

    collections = [args.collection] if args.collection else collections_acronym()

    run(collections, args.all_records)
