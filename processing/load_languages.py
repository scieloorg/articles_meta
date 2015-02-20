# coding: utf-8
"""
This scripts loads a list of PDF, Translation HTML's and XML's available
in a given SciELO Website and try to figure out the available versions of the
fulltexts for each SciELO Document stored into the ArticleMeta.

The lists of PDF, HTML's and XML's must be available in the SciELO Website
according to the following examples:

PDF: http://www.scielo.br/static_pdf_catalog.txt
Translation HTML: http://www.scielo.br/static_html_catalog.txt
XML: http://www.scielo.br/static_xml_catalog.txt
"""
from datetime import datetime, timedelta
import argparse
import logging
import requests

from xylose.scielodocument import Article

FROM = datetime.now() - timedelta(days=15)
FROM.isoformat()[:10]

ARTICLEMETA = 'http://articlemeta.scielo.org/api/v1/'

def _config_logging(logging_level='INFO', logging_file=None):

    allowed_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    logging_config = {
        'level': allowed_levels.get(logging_level, 'INFO'),
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }

    if logging_file:
        logging_config['filename'] = logging_file

    logging.basicConfig(**logging_config)

def do_request(url):

    logging.debug('Loading url: %s' % url)
    document = requests.get(url)

    return document.json()


COLLECTIONS = do_request('%scollection' % (ARTICLEMETA))


def collection_info(collection):
    info = {}
    for item in COLLECTIONS:
        if item['acron'] == collection:
            return item


def load_documents(collection, from_date=FROM, identifiers=True):
    mode='history'
    if identifiers:
        mode = 'identifiers'

    offset=0
    while True:
        url = '%sarticle/%s/?collection=%s&offset=%s' % (ARTICLEMETA, mode, collection, str(offset))
        identifiers = do_request(url)

        if len(identifiers['objects']) == 0:
            raise StopIteration

        for identifier in identifiers['objects']:
            
            if 'event' in identifier and not identifier['event'] in ['add', 'update']:
                continue

            code = identifier['code']
            collection = identifier['collection']
            url_document = '%sarticle?collection=%s&code=%s' % (ARTICLEMETA, collection, code)

            data = do_request(url_document)

            if not data:
                continue

            document = Article(data)

            yield document

        offset+=1000

def main(collection, from_date, identifiers):

    coll_info = collection_info(collection)

    logging.info('Loading languages for %s' % coll_info['domain'])
    logging.info('Using mode identifiers %s' % str(identifiers))

    for document in load_documents(collection, from_date, identifiers):
        logging.debug('checking languages for %s' % document.publisher_id)
        print 'checking languages for %s' % document.publisher_id

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Load Languages from SciELO static files available in the file system"
    )

    parser.add_argument(
        '--collection',
        '-c',
        choices=[i['code'] for i in COLLECTIONS],
        required=True,
        help='Collection acronym'
    )

    parser.add_argument(
        '--from_date',
        '-f',
        default=FROM,
        help='ISO date like 2013-12-31'
    )

    parser.add_argument(
        '--identifiers',
        '-i',
        action='store_true',
        help='Define the identifiers endpoint to retrieve the document and journal codes. If not given the enpoint used will be the history. When using history the processing will also remove records from the index.'
    )

    parser.add_argument(
        '--logging_file',
        '-o',
        default='/var/log/articlemeta/load_languages.log',
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

    main(args.collection, args.from_date, args.identifiers)
