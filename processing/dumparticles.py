# coding: utf-8
"""
This scripts uses the Article Meta API to harvest all SciELO Network Documents
They are stored into a zip file.
This processing always harvest the entire database to garantee that all the 
documents are up to date.
"""
import logging
import zipfile
import datetime

import requests
import argparse

ARTICLEMETA = 'http://192.168.1.162:7000/api/v1/'

def load_documents():
    offset=0
    while True:
        url = '%sarticle/identifiers?offset=%s' % (ARTICLEMETA, str(offset))
        logging.debug('Loading url: %s' % url)
        identifiers = requests.get(url).json()

        if len(identifiers['objects']) == 0:
            raise StopIteration

        for identifier in identifiers['objects']:
            code = identifier['code']
            collection = identifier['collection']
            url_document = '%sarticle?code=%s&format=xmlwos' % (ARTICLEMETA, code)
            logging.debug('Loading url: %s' % url_document)
            document = requests.get(url_document)
            yield ('%s_%s' % (collection, code), document.text)

        offset+=1000

def dumpdata(*args, **xargs):
    zip_name = xargs['file_name']

    logging.debug('Creating zip file: %s' % zip_name)
    with zipfile.ZipFile(zip_name, 'w', allowZip64=True) as thezip:
        for document in load_documents():
            xml_file_name = '%s.xml' % document[0]
            thezip.writestr(xml_file_name, bytes(document[1].encode('utf-8')))
        
        readme = bytes("Documents updated at:" % datetime.datetime.now().isoformat())

        thezip.writestr("README.txt", readme)

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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Dump SciELO Network metadata"
    )

    parser.add_argument(
        '--zip_file',
        '-f',
        default='/tmp/dumpdata.zip',
        help='Full path to the zip file that will receive the documents'
    )

    parser.add_argument(
        '--logging_file',
        '-o',
        default='/tmp/dumpdata.log',
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

    dumpdata(
        file_name=args.zip_file
    )