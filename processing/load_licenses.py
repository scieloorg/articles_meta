# coding: utf-8
"""
This scripts scrapy the use licenses of the scielo documents from the website
and load them into the Articlemeta, this process is necessary because the
legacy databases does not have the licenses persisted for each document.
"""
import os
import logging
import logging.config
import re
import argparse
from datetime import datetime, timedelta
import requests

from pymongo import MongoClient
from xylose.scielodocument import Article
from articlemeta import utils

logger = logging.getLogger(__name__)
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
MONGODB_HOST = os.environ.get('MONGODB_HOST', None)

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
        'processing.load_licenses': {
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

LICENSE_A_REGEX = re.compile(r'<a.*?creativecommons.org/licenses/(?P<license>.*?/\d+\.\d+).*?>')
LICENSE_IMG_REGEX = re.compile(r'<img.*?creativecommons.org/l/(?P<license>.*?/\d+\.\d+).*?>')

allowed_licenses = ['by', 'by-nc', 'by-nd', 'by-sa', 'by-nc-sa', 'by-nc-nd']

config = utils.Configuration.from_env()
settings = dict(config.items())

try:
    articlemeta_db = MongoClient(MONGODB_HOST)['articlemeta']
except:
    logging.error('Fail to connect to (%s)', settings['app:main']['mongo_uri'])


def collections_acronym():

    collections = articlemeta_db['collections'].find({}, {'_id': 0})

    return [i['code'] for i in collections]


def collection_info(collection):

    info = articlemeta_db['collections'].find_one(
        {'acron': collection}, {'_id': 0})

    return info


def load_documents(collection, all_records=False):

    fltr = {
        'collection': collection
    }

    if all_records is False:
        fltr['license'] = {'$exists': 0}

    documents = articlemeta_db['articles'].find(
        fltr,
        {'code': 1}
    )

    pids = []
    for document in documents:
        pids.append(document['code'])

    if 'license' in fltr:
        del(fltr['license'])

    for pid in pids:
        fltr['code'] = pid
        document = articlemeta_db['articles'].find_one(
            fltr,
            {'_id': 0, 'citations': 0}
        )
        yield Article(document)

    documents.close()  # Release the cursor once it has no timeout.


def do_request(url, json=True):

    headers = {
        'User-Agent': 'SciELO Processing ArticleMeta: LoadLicense'
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


def scrap_license(data):

    result = LICENSE_IMG_REGEX.search(data) or LICENSE_A_REGEX.search(data)

    if not result:
        return None

    lc = result.groupdict().get('license', None)
    if lc.split('/')[0] in allowed_licenses:
        return lc


def run(collections, all_records=False):

    if not isinstance(collections, list):
        logger.error('Collections must be a list o collection acronym')
        exit()

    for collection in collections:
        coll_info = collection_info(collection)

        logger.info(u'Loading licenses for %s', coll_info['domain'])
        logger.info(u'Using mode all_records %s', str(all_records))

        for document in load_documents(collection, all_records=all_records):

            lic = None
            try:
                lic = scrap_license(
                    do_request(
                        document.html_url(), json=False
                    )
                )
            except:
                logger.error('Fail to scrap: %s', document.publisher_id)
                continue

            if not lic:
                logger.debug('No license defined for: %s', document.publisher_id)
                continue

            articlemeta_db['articles'].update(
                {'code': document.publisher_id, 'collection': document.collection_acronym},
                {'$set': {'license': lic}}
            )

            logger.debug('%s: %s', document.publisher_id, lic)


def main():
    parser = argparse.ArgumentParser(
        description="Load documents license from SciELO website"
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
        default='DEBUG',
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
