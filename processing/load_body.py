# coding: utf-8
"""
This scripts scrapy the use licenses of the scielo documents from the website
and load them into the Articlemeta, this process is necessary because the
legacy databases does not have the licenses persisted for each document.
"""
import re
import os
import argparse
import logging
import logging.config
from datetime import datetime, timedelta

import chardet
import requests
from lxml import etree
from io import StringIO

from pymongo import MongoClient
from xylose.scielodocument import Article

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
        'processing.load_body': {
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

BODY_REGEX = re.compile(r'<div .*class="index,(?P<language>.*?)">(?P<body>.*)</div>')
REMOVE_LINKS_REGEX = re.compile(r'\[.<a href="javascript\:void\(0\);".*?>Links</a>.\]', re.IGNORECASE)

try:
    articlemeta_db = MongoClient(MONGODB_HOST)['articlemeta']
except:
    logging.error('Fail to connect to (%s)', MONGODB_HOST)


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

    if not all_records:
        fltr['body'] = {'$exists': 0}

    documents = articlemeta_db['articles'].find(
        fltr,
        {'code': 1},
    )

    if 'body' in fltr:
        del(fltr['body'])

    pids = []
    for document in documents:
        pids.append(document['code'])

    for pid in pids:
        fltr['code'] = pid
        document = articlemeta_db['articles'].find_one(
            fltr,
            {'_id': 0, 'citations': 0}
        )
        yield Article(document)

    documents.close()


def do_request(url, json=True):

    headers = {
        'User-Agent': 'SciELO Processing ArticleMeta: LoadBody'
    }

    try:
        document = requests.get(url, headers=headers)
    except:
        logger.error(u'HTTP request error for: %s', url)
    else:
        if json:
            return document.json()
        else:
            return document.content


def scrap_body(data, language):
    '''
    Function to scrap article by URL and slice the important content.

    Params:
    :param data: bytes, encoded by source
    :param language: str [en, es, pt, ...]

    Return the unicode of the body encoded by etree.tostring line 178
    '''

    encoding = chardet.detect(data)['encoding']

    #  IMPORTANTE: Nesse trecho estamos decodificando para o encoding descoberto
    #  pelo chardet e substituindo os caracteres que não foram encontrados no
    #  encoding por código unicode.
    data = data.decode(encoding, 'replace')

    data = ' '.join([i.strip() for i in data.split('\n')])

    parser = etree.HTMLParser(remove_blank_text=True)
    tree = etree.parse(StringIO(data), parser)

    etree_body = tree.find('.//div[@class="content"]/div[@class="index,%s"]' % language)

    if etree_body is None:
        logger.debug('Body not found')
        return None

    lic = etree_body.find('./div[@class="article-license"]')
    if lic is not None:
        etree_body.remove(lic)

    lic = etree_body.find('./div[@class="license"]')
    if lic is not None:
        etree_body.remove(lic)

    parsed_body = etree.tostring(etree_body, encoding='unicode', pretty_print=False).rstrip('\r\n')

    if not parsed_body:
        logger.debug('Body not found')
        return None

    result = BODY_REGEX.search(parsed_body)

    if not result:
        logger.debug('Body not found')
        return None

    body = result.groupdict().get('body', None).strip()

    # Removing Reference links

    body = REMOVE_LINKS_REGEX.sub(' ', body)

    return body


def run(collections, all_records=False):

    if not isinstance(collections, list):
        logger.error('Collections must be a list o collection acronym')
        exit()

    for collection in collections:

        coll_info = collection_info(collection)

        logger.info(u'Loading body for %s', coll_info['domain'])
        logger.info(u'Using mode all_records %s', str(all_records))

        for document in load_documents(collection, all_records=all_records):

            fulltexts = document.fulltexts()
            if not fulltexts:
                logger.debug('Fulltexts not availiable for %s, %s', collection, document.publisher_id)
                continue

            html_fulltexts = fulltexts.get('html', None)

            if not html_fulltexts:
                logger.debug('HTML Fulltexts not availiable for %s, %s', collection, document.publisher_id)
                continue

            bodies = {}
            for language, url in html_fulltexts.items():

                try:
                    body = scrap_body(do_request(url, json=False), language)
                except Exception as exc:
                    logger.error('Fail to scrap: %s, %s, %s', collection, document.publisher_id, language)
                    logger.exception(exc)
                    continue

                if not body:
                    logger.error('No body defined for: %s, %s, %s', collection, document.publisher_id, language)
                    continue

                bodies[language] = body

            if len(bodies) < len(html_fulltexts):
                logger.error('Fail to scrap some of the documents for: %s, %s', collection, document.publisher_id)
                continue

            if len(bodies) == 0:
                logger.error('No bodies found for: %s, %s', collection, document.publisher_id)
                continue

            articlemeta_db['articles'].update(
                {'code': document.publisher_id, 'collection': document.collection_acronym},
                {'$set': {'body': bodies}}
            )

            logger.debug('Bodies collected for: %s, %s', collection, document.publisher_id)


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
        help='Apply processing to all records or just records without the body parameter'
    )

    parser.add_argument(
        '--logging_file',
        '-o',
        help='Full path to the log file'
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
