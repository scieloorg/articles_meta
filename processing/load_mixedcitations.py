# coding: utf-8
"""
This scripts loads the mixed citations of a given article.
"""
import argparse
import logging
import codecs
import json
import unicodedata

from pymongo import MongoClient
from articlemeta import utils
from xylose.scielodocument import Article

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


try:
    articlemeta_db = MongoClient(MONGODB_HOST)
except:
    raise ValueError('Fail to connect to (%s)', MONGODB_HOST)


def remove_control_characters(data):
    return "".join(ch for ch in data if unicodedata.category(ch)[0] != "C")


def html_decode(string):

    string = remove_control_characters(string)

    return string


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


def audity(mixed, document):
    logger.debug('Auditing mixed citation')

    if int(mixed['order']) > len(document.citations or []):
        return False

    check = mixed['mixed'].lower()
    citation_index = int(mixed['order'])-1
    citation_titles = [i.lower() for i in [
        document.citations[citation_index].title() or '',
        document.citations[citation_index].source or '',
        document.citations[citation_index].chapter_title or '',
        document.citations[citation_index].article_title or '',
        document.citations[citation_index].thesis_title or '',
        document.citations[citation_index].link_title or '',
        document.citations[citation_index].issue_title or '',
        document.citations[citation_index].conference_title or ''
    ] if i]

    citation_authors = document.citations[citation_index].authors or []

    for title in citation_titles:
        if title in check:
            return True

    for author in citation_authors:
        if author.get('surname', '').lower() in check:
            return True
        if author.get('given_names', '').lower() in check:
            return True

    return False


def get_document(collection, code):
    logger.debug('Loading document from database')

    document = articlemeta_db['articles'].find_one({'collection': collection, 'code': code})

    if not document:
        return

    return Article(document)


def update_document(mixed, document):
    logger.debug('Updating citation in database')

    citation_field = 'citations.%s.mixed' % str(int(mixed['order'])-1)
    articlemeta_db['articles'].update(
        {
            'collection': document.collection_acronym,
            'code': document.publisher_id
        },
        {
            '$set': {
                citation_field: mixed['mixed']
            }
        }
    )


def run(mixed_citations_file, import_data):

    with codecs.open(mixed_citations_file, encoding='utf-8') as mixed_citations:

        for line in mixed_citations:
            mixed = json.loads(line)
            mixed['mixed'] = html_decode(mixed['mixed'])
            document = get_document(mixed['collection'], mixed['pid'])

            logger.info('Trying to import %s %s %s', mixed['collection'], mixed['pid'], mixed['order'])
            if not document:
                logger.error('Document not found in Article Meta %s %s %s', mixed['collection'], mixed['pid'], mixed['order'])
                continue

            if not audity(mixed, document):
                logger.error('Document did not pass in auditory %s %s %s', mixed['collection'], mixed['pid'], mixed['order'])
                continue

            logger.debug('Document pass in auditory %s %s %s', mixed['collection'], mixed['pid'], mixed['order'])

            if import_data:
                logger.debug('Importing data for %s %s %s', mixed['collection'], mixed['pid'], mixed['order'])
                update_document(mixed, document)


def main():
    parser = argparse.ArgumentParser(
        description="Load mixed citations according to a given json file"
    )

    parser.add_argument(
        '--csv_file',
        '-f',
        help='A json file with the mixed citations of each article'
    )

    parser.add_argument(
        '--import_data',
        '-i',
        action='store_true',
        help='Import data'
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

    run(args.csv_file, args.import_data)
