# coding: utf-8
"""
This scripts loads the issue section whiting a given article.
The lists of Sections must be given and respect the following format.
"collection acronym","language","code","text"
"""
import os
import re
import sys
import argparse
import logging
from datetime import datetime, timedelta

import requests
from xylose.scielodocument import Article

from articlemeta import controller


logger = logging.getLogger(__name__)

FROM = datetime.now() - timedelta(days=15)
FROM = FROM.isoformat()[:10]

file_regex = re.compile(r'serial.*.htm|.*.xml')
data_struct_regex = re.compile(r'^fulltexts\.(pdf|html)\.[a-z][a-z]$')


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


def collections_acronym(articlemeta_db):

    collections = articlemeta_db['collections'].find({}, {'_id': 0})

    return [i['code'] for i in collections]


def collection_info(articlemeta_db, collection):

    info = articlemeta_db['collections'].find_one({'acron': collection}, {'_id': 0})

    return info


def do_request(url, json=True):

    headers = {
        'User-Agent': 'SciELO Processing ArticleMeta: LoadSection'
    }

    document = None
    try:
        document = requests.get(url, headers=headers)
    except:
        logger.error(u'HTTP request error for: %s', url)

    if document.status_code == 404:
        logger.error(u'Data not found for: %s', url)
        return None

    if json:
        return document.json()
    else:
        return document


def load_documents(articlemeta_db, collection, all_records=False):

    fltr = {
        'collection': collection
    }

    if all_records is False:
        fltr['section'] = {'$exists': 0}

    documents = articlemeta_db['articles'].find(
        fltr,
        {'code': 1}
    )

    pids = []
    for document in documents:
        pids.append(document['code'])

    if 'section' in fltr:
        del(fltr['section'])

    for pid in pids:
        fltr['code'] = pid
        document = articlemeta_db['articles'].find_one(
            fltr,
            {'_id': 0, 'citations': 0},
            no_cursor_timeout=True
        )
        yield Article(document)

    documents.close()


class StaticCatalog(object):

    def __init__(self, collection):
        self.catalog = self._load_static_catalog(collection)

    def _load_static_catalog(self, source):
        """
        source: www.scielo.br
        type: in ['section']

        Download the static files text lists from the selected SciELO Domain.
        Parse the txt file to produce a dictionary with the following structure:
        {
            'ven': {
                'code': {
                    'pt': 'section pt',
                    'es': 'section es',
                    ]
                }
            },
            ...
        }
        """

        logger.info(u'Loading static_section_catalog.txt from server %s', source['domain'])

        url = '/'.join(['http:/', source['domain'], 'static_section_catalog.txt'])
        content = do_request(url, json=False)

        if not content:
            logger.warning(u'Section catalog not found: %s', url)
            return None

        items = set([i for i in content.iter_lines(decode_unicode='utf-8')])

        sections = {}
        for line in sorted(items):
            splited_line = [i.strip() for i in line.split('|')]
            if len(splited_line) != 4:
                continue
            issue = splited_line[0]
            language = splited_line[1]
            code = splited_line[2]
            label = splited_line[3]

            sections.setdefault(issue, {})
            sections[issue].setdefault(code, {})
            sections[issue][code].update({language: label})

        return sections

    def get_section_available(self, pid, issue, section_code):
        """
        This method checks the existence of the section agains the catalog.
        collection: scl <acronym 3 letters>
        issue: 1690-751520090003 <PID SciELO for issues>
        code: ENL010 <section legacy code>
        """
        logger.debug(
            u'Checking sessions in %s, %s for %s',
            issue,
            section_code,
            pid
        )

        try:
            section = self.catalog[issue][section_code]
        except:
            logger.warning(
                u'Session not found int catalog for %s, %s for %s',
                issue,
                section_code,
                pid
            )
            return None

        if len(section) == 0:
            return None

        return section

    def section(self, document):
        """
        This method retrieve a dictionary of the available section of a given
        document
        input:
            xylose.scielo_document.Article()
        output:
            {
                'pt': 'label',
                'es': 'label'
            }
        """
        pid = document.publisher_id
        issue_pid = document.publisher_id[1:18]
        section_code = document.section_code

        section = self.get_section_available(pid, issue_pid, section_code)

        if not section:
            return None

        return section


def run(articlemeta_db, collections, all_records=False):

    if not isinstance(collections, list):
        logger.error('Collections must be a list of collection acronym')
        exit()

    for collection in collections:

        coll_info = collection_info(articlemeta_db, collection)

        logger.info(u'Loading sections for %s', coll_info['domain'])
        logger.info(u'Using mode all_records %s', str(all_records))

        static_catalogs = StaticCatalog(coll_info)

        if not static_catalogs.catalog:
            logger.info(u'Section Catalog not found for: %s Processing Interrupited', coll_info['domain'])
            exit()

        for document in load_documents(articlemeta_db, collection, all_records=all_records):
            logger.debug(
                u'Checking section for %s_%s',
                collection,
                document.publisher_id
            )

            section = static_catalogs.section(document)

            if not isinstance(section, dict):
                logger.warning(
                    u'Section not loaded for %s_%s',
                    collection,
                    document.publisher_id
                )
                continue

            articlemeta_db['articles'].update(
                {'code': document.publisher_id, 'collection': document.collection_acronym},
                {'$set': {'section': section}}
            )

            logger.debug(
                u'Update made for %s_%s',
                collection,
                document.publisher_id
            )


def main():
    db_dsn = os.environ.get('MONGODB_HOST', 'mongodb://localhost:27017/articlemeta')
    try:
        articlemeta_db = controller.get_dbconn(db_dsn)
    except:
        print('Fail to connect to:', db_dsn)
        sys.exit(1)

    _collections_acronyms = collections_acronym(articlemeta_db)

    parser = argparse.ArgumentParser(
        description="Load Languages from SciELO static files available in the file system"
    )

    parser.add_argument(
        '--collection',
        '-c',
        choices=_collections_acronyms,
        help='Collection acronym'
    )

    parser.add_argument(
        '--all_records',
        '-a',
        action='store_true',
        help='Apply processing to all records or just records without the section parameter'
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

    collections = [args.collection] if args.collection else _collections_acronyms

    run(articlemeta_db, collections, args.all_records)
