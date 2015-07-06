# coding: utf-8
"""
This scripts scrapy the use licenses of the scielo documents from the website
and load them into the Articlemeta, this process is necessary because the
legacy databases does not have the licenses persisted for each document.
"""
import logging
import re
import argparse
from datetime import datetime, timedelta
import requests
from lxml import etree
from StringIO import StringIO
import HTMLParser

from pymongo import MongoClient
from xylose.scielodocument import Article
from articlemeta import utils

logger = logging.getLogger(__name__)

FROM = datetime.now() - timedelta(days=15)
FROM.isoformat()[:10]

BODY_REGEX = re.compile(r'<div class="index,(?P<language>.*?)">(?P<body>.*)</div>')
REMOVE_LINKS_REGEX = re.compile(r'\[.<a href="javascript\:void\(0\);".*?>Links</a>.\]', re.IGNORECASE)

config = utils.Configuration.from_env()
settings = dict(config.items())

try:
    articlemeta_db = MongoClient(settings['app:main']['mongo_uri'])['articlemeta']
except:
    logging.error('Fail to connect to (%s)' % settings['app:main']['mongo_uri'])

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
        fltr['body'] = {'$exists': 0}

    documents = articlemeta_db['articles'].find(
        fltr,
        {'_id': 0, 'citations': 0}
    )

    for document in documents:
        yield Article(document)


def _config_logging(logging_level='INFO', logging_file=None):

    allowed_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    
    logger.setLevel(allowed_levels.get(logging_level, 'INFO'))

    if logging_file:
        hl = logging.FileHandler(logging_file, mode='a')
    else:
        hl = logging.StreamHandler()

    hl.setFormatter(formatter)
    hl.setLevel(allowed_levels.get(logging_level, 'INFO'))

    logger.addHandler(hl)

    return logger


def do_request(url, json=True):

    try:
        document = requests.get(url)
    except:
        logger.error(u'HTTP request error for: %s' % url)
    else:
        if json:
            return document.json()
        else:
            return document.text

def scrap_body(data, language):

    # html_parser = HTMLParser.HTMLParser()
    # unescaped = html_parser.unescape(data)

    data = ' '.join([i.strip() for i in data.split('\n')])

    parser = etree.HTMLParser(remove_blank_text=True)
    tree = etree.parse(StringIO(data), parser)

    etree_body = tree.find('.//div[@class="content"]/div[@class="index,%s"]' % language)

    if etree_body is None:
        logger.debug('Body not found')
        return None

    lic = etree_body.find('./div[@class="article-license"]')
    if lic != None:
        etree_body.remove(lic)

    parsed_body = etree.tostring(etree_body, encoding='unicode', pretty_print=False).rstrip('\r\n')

    if not parsed_body:
        logger.debug('Body not found')
        return None

    result = BODY_REGEX.search(parsed_body)

    if not result:
        logger.debug('Body not found')
        return None

    body_language = result.groupdict().get('language', None)

    body = result.groupdict().get('body', None).strip()

    ## Removing Reference links

    body = REMOVE_LINKS_REGEX.sub(' ', body)
    
    return body

def run(collection, all_records):

    coll_info = collection_info(collection)

    logger.info(u'Loading body for %s' % coll_info['domain'])
    logger.info(u'Using mode all_records %s' % str(all_records))

    for document in load_documents(collection, all_records=all_records):

        fulltexts = document.fulltexts()
        if not fulltexts:
            logger.debug('Fulltexts not availiable for %s' % document.publisher_id)
            continue

        html_fulltexts = fulltexts.get('html', None)

        if not html_fulltexts:
            logger.debug('HTML Fulltexts not availiable for %s' % document.publisher_id)
            continue

        bodies = {}
        for language, url in html_fulltexts.items():        
    
            try:
                body = scrap_body(do_request(url, json=False), language)
            except:
                logger.error('Fail to scrap: %s, %s' % (document.publisher_id, language))
                continue

            if not body:
                logger.error('No body defined for: %s, %s' % (document.publisher_id, language))
                continue

            bodies[language] = body

        if len(bodies) < len(html_fulltexts):
            logger.error('Fail to scrap some of the documents for: %s' % (document.publisher_id))
            continue

        if len(bodies) == 0:
            logger.error('No bodies found for: %s' % (document.publisher_id))
            continue

        articlemeta_db['articles'].update(
            {'code': document.publisher_id,'collection': document.collection_acronym}, 
            {'$set': {'body': bodies}}
        )

        logger.debug('Bodies colected for: %s' % (document.publisher_id))

def main():
    parser = argparse.ArgumentParser(
        description="Load documents license from SciELO website"
    )

    parser.add_argument(
        '--collection',
        '-c',
        choices=collections_acronym(),
        required=True,
        help='Collection acronym'
    )

    parser.add_argument(
        '--all_records',
        '-a',
        action='store_true',
        help='Apply processing to all records or just records without the license parameter'
    )

    parser.add_argument(
        '--logging_file',
        '-o',
        help='Full path to the log file'
    )

    parser.add_argument(
        '--logging_level',
        '-l',
        default='DEBUG',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logggin level'
    )

    args = parser.parse_args()

    _config_logging(args.logging_level, args.logging_file)

    run(args.collection, args.all_records)