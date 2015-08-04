# coding: utf-8
"""
This scripts scrapy the DOI of the scielo documents from the website
and load them into the Articlemeta, this process is necessary because the
legacy databases does not have the doi persisted for each document.
"""
import logging
import re
import argparse
from datetime import datetime, timedelta
import requests
from lxml import etree
from StringIO import StringIO
from pymongo import MongoClient
from xylose.scielodocument import Article
from articlemeta import utils

logger = logging.getLogger(__name__)

FROM = datetime.now() - timedelta(days=15)
FROM.isoformat()[:10]

DOI_REGEX = re.compile(r'<a.*?creativecommons.org/licenses/(?P<license>.*?/\d+\.\d+).*?>')

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
        fltr['license'] = {'$exists': 0}

    documents = articlemeta_db['articles'].find(
        fltr,
        {'_id': 0, 'citations': 0}
    ).limit(10)

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

    headers = {
        'User-Agent': 'SciELO Processing ArticleMeta: LoadDoi'
    }

    try:
        document = requests.get(url, headers=headers)
    except:
        logger.error(u'HTTP request error for: %s' % url)
    else:
        if json:
            return document.json()
        else:
            return document.text

def scrap_doi(data):

    data = ' '.join([i.strip() for i in data.split('\n')])

    parser = etree.HTMLParser(remove_blank_text=True)
    tree = etree.parse(StringIO(data), parser)

    etree_doi = tree.find('.//h4[@id="doi"]')

    if etree_doi is None:
        logger.debug('DOI not found')
        return None

    result = etree_doi.text.strip().replace('http://dx.doi.org/', '')

    if not result:
        return None

    return result

def run(collections, all_records=False):

    if not isinstance(collections, list):
        logger.error('Collections must be a list o collection acronym')
        exit()

    for collection in collections:
        coll_info = collection_info(collection)

        logger.info(u'Loading DOI for %s' % coll_info['domain'])
        logger.info(u'Using mode all_records %s' % str(all_records))

        for document in load_documents(collection, all_records=all_records):

            doi = None
            try:
                doi = scrap_license(
                    do_request(
                        document.html_url(), json=False
                    )
                )
            except:
                logger.error('Fail to scrap: %s' % document.publisher_id)
                continue

            if not doi:
                logger.debug('No DOI defined for: %s' % document.publisher_id)
                continue

            # articlemeta_db['articles'].update(
            #     {'code': document.publisher_id,'collection': document.collection_acronym}, 
            #     {'$set': {'doi': doi}}
            # )

            logger.debug('%s: %s' % (document.publisher_id, license))

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

    collections = [args.collection] if args.collection else collections_acronym()

    run(collections, args.all_records)
