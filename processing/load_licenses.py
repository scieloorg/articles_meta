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

from pymongo import MongoClient
from xylose.scielodocument import Article
from articlemeta import utils

logger = logging.getLogger(__name__)

FROM = datetime.now() - timedelta(days=15)
FROM.isoformat()[:10]

LICENSE_A_REGEX = re.compile(r'<a.*?creativecommons.org/licenses/(?P<license>.*?/\d+\.\d+).*?>')
LICENSE_IMG_REGEX = re.compile(r'<img.*?creativecommons.org/l/(?P<license>.*?/\d+\.\d+).*?>')

allowed_licenses = ['by', 'by-nc', 'by-nd', 'by-sa', 'by-nc-sa', 'by-nc-nd']

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

def scrap_license(data):

    result = LICENSE_IMG_REGEX.search(data) or LICENSE_A_REGEX.search(data)

    if not result:
        return None

    lc = result.groupdict().get('license', None)
    if lc.split('/')[0] in allowed_licenses:
        return lc

def run(collection, all_records):

    coll_info = collection_info(collection)

    logger.info(u'Loading languages for %s' % coll_info['domain'])
    logger.info(u'Using mode all_records %s' % str(all_records))

    for document in load_documents(collection, all_records=all_records):

        license = None
        try:
            license = scrap_license(
                do_request(
                    document.html_url(), json=False
                )
            )
        except:
            logger.error('Fail to scrap: %s' % document.publisher_id)
            continue

        if not license:
            continue

        articlemeta_db['articles'].update(
            {'code': document.publisher_id,'collection': document.collection_acronym}, 
            {'$set': {'license': license}}
        )

        logger.debug('%s: %s' % (document.publisher_id, license))

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