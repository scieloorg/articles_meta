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
import re
import os
import sys
import argparse
import logging
import logging.config
from datetime import datetime, timedelta

import requests
from articlemeta import utils
from articlemeta import controller
from xylose.scielodocument import Article

logger = logging.getLogger(__name__)
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')

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
        'processing.load_languages': {
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

file_regex = re.compile(r'serial.*.htm|.*.xml')
data_struct_regex = re.compile(r'^fulltexts\.(pdf|html)\.[a-z][a-z]$')


def collections_acronym(articlemeta_db):

    collections = articlemeta_db['collections'].find({}, {'_id': 0})

    return [i['code'] for i in collections]


def collection_info(collection, articlemeta_db):

    info = articlemeta_db['collections'].find_one({'acron': collection}, {'_id': 0})

    return info


def do_request(url, json=True):

    headers = {
        'User-Agent': 'SciELO Processing ArticleMeta: LoadLanguage'
    }

    try:
        document = requests.get(url, headers=headers)
    except:
        logger.error(u'HTTP request error for: %s', url)
    else:
        if json:
            return document.json()
        else:
            return document


def load_documents(collection, articlemeta_db, all_records=False):

    fltr = {
        'collection': collection
    }

    if all_records is False:
        fltr['fulltexts'] = {'$exists': 0}

    documents = articlemeta_db['articles'].find(
        fltr,
        {'code': 1}
    )

    pids = []
    for document in documents:
        pids.append(document['code'])

    if 'fulltexts' in fltr:
        del(fltr['fulltexts'])

    for pid in pids:
        fltr['code'] = pid
        document = articlemeta_db['articles'].find_one(
            fltr,
            {'_id': 0, 'citations': 0}
        )
        yield Article(document)

    documents.close()


class StaticCatalog(object):

    def __init__(self, collection):
        self.catalog = {}
        self._load_static_catalog(collection, 'pdf')
        self._load_static_catalog(collection, 'html')
        self._load_static_catalog(collection, 'xml')

    def _load_static_catalog(self, source, tipe):
        """
        source: www.scielo.br
        type: in ['pdf', 'html', 'xml']

        Download the static files text lists from the selected SciELO Domain.
        Parse the txt file to produce a dictionary with the following structure:
        {
            'jbco': {
                'v6n3': {
                    'pdf': [
                        '0001',
                        '0002',
                        '0003',
                        '0004',
                        'en_0004',
                        ...
                    ],
                    'html': [
                        '0001',
                        '0002',
                        '0003',
                        '0004',
                        'en_0004',
                        ...
                    ]
                }
            },
            ...
        }
        """

        logger.info(u'Loading static_%s_files.txt from server %s', tipe, source)

        filename = 'static_%s_files.txt' % tipe

        url = '/'.join(['http:/', source, filename])

        content = do_request(url, json=False).iter_lines(decode_unicode='utf-8')

        for line in sorted([i for i in content]):
            splitedline = line.lower().split('/')[1:]
            if not len(splitedline) == 3:
                continue
            self.catalog.setdefault(splitedline[0], {})
            self.catalog[splitedline[0]].setdefault(splitedline[1], {'pdf': [], 'html': [], 'xml': []})
            self.catalog[splitedline[0]][splitedline[1]][tipe].append(splitedline[2].replace('.html', '.htm')[:-4])

    def _file_id(self, file_code):
        file_code = file_code.lower().replace('/', '___').replace('\\', '___')

        try:
            file_code = file_regex.search(
                file_code
            ).group().replace(
                'serial___', '').replace('markup___', '').split('___')
        except:
            logger.error(u'Fail to parse the file_id for %s', file_code)
            return None

        file_code[2] = file_code[2].replace('.html', '.htm')[:-4]

        return file_code

    def _file_name(self, file_code):
        file_code = file_code.replace('/', '___').replace('\\', '___')
        file_code = file_code.replace('.html', '.htm')

        return file_code.split('___')[-1][:-4]

    def is_file_available(self, file_id, tipe, language, original_language):
        """
        This method checks the existence of the file_id agains the catalog.
        file_id:
            Is a array with the keys to find a file inside the catalog.
            Ex:
                ['rsp', 'v48n6', '0034-8910-rsp-48-6-0873']
        language:
            ISO 2 letters.
        tipe:
            'html' or 'pdf'
        """
        logger.debug(
            u'Checking fulltexts in %s %s for %s, %s, %s',
            tipe,
            language,
            file_id[0],
            file_id[1],
            file_id[2]
        )

        if language == original_language:
            file_name = file_id[2]
        else:
            file_name = '_'.join([language, file_id[2]])

        files = []
        try:
            files = self.catalog[file_id[0]][file_id[1]][tipe]
        except:
            logger.warning(
                u'Issue not found int catalog for %s %s for %s, %s, %s',
                tipe,
                language,
                file_id[0],
                file_id[1],
                file_id[2]
            )

        if file_name.lower() in files:
            return True

        return False

    def fulltexts(self, document):
        """
        This method retrieve a dictionary of the available fulltexts in each
        document type ['pdf', 'html', 'xml']
        input:
            xylose.scielo_document.Article()
            ex:
                output:
                {
                    'pdf': {
                        'pt': 'url',
                        'es': 'url',
                        'en': 'url'
                    },
                    'html': {
                        'pt': 'url',
                        'es': 'url',
                        'en': 'url'
                    }
                }
        """

        file_id = self._file_id(document.file_code(fullpath=True))

        if not file_id:
            logger.error(u'Fail to parse file_id for %s_%s', document.collection_acronym, document.publisher_id)
            return None

        if not document.journal.languages:
            logger.info(u'Journal without publication languages defined %s', file_id[0])
            return None

        data = {'fulltexts.pdf': set(), 'fulltexts.html': set()}
        data['fulltexts.html'].add(document.original_language()) # Original language must have fulltext in html.
        if document.data_model_version == 'xml':
            for lang in document.xml_languages() or []:
                data['fulltexts.html'].add(lang)

        languages = document.journal.languages + document.languages()
        languages.append(document.original_language())

        for language in set(languages):
            if self.is_file_available(file_id, 'pdf', language, document.original_language()):
                data['fulltexts.pdf'].add(language)
                logger.info(
                    u'Fulltext available in pdf %s for %s, %s, %s',
                    language,
                    file_id[0],
                    file_id[1],
                    file_id[2]
                )

            if self.is_file_available(file_id, 'html', language, document.original_language()):
                data['fulltexts.html'].add(language)
                logger.info(
                    u'Fulltext available in html %s for %s, %s, %s',
                    language,
                    file_id[0],
                    file_id[1],
                    file_id[2]
                )

        ldata = {}

        if len(data['fulltexts.pdf']) > 0:
            for lang in data['fulltexts.pdf']:
                if lang != document.original_language():
                    fname = '_'.join([
                        lang,
                        self._file_name(document.file_code(fullpath=True))]
                    )
                else:
                    fname = self._file_name(document.file_code(fullpath=True))

                ldata['fulltexts.pdf.%s' % lang] = 'http://%s' % '/'.join([
                    document.scielo_domain,
                    'pdf',
                    file_id[0],
                    file_id[1],
                    '%s.pdf' % fname
                    ]
                )

        if len(data['fulltexts.html']) > 0:
            for lang in data['fulltexts.html']:
                ldata['fulltexts.html.%s' % lang] = 'http://%s/scielo.php?script=sci_arttext&pid=%s&tlng=%s' % (
                    document.scielo_domain,
                    document.publisher_id,
                    lang
                )

        return ldata


def run(collections, articlemeta_db, all_records=False):

    if not isinstance(collections, list):
        logger.error('Collections must be a list o collection acronym')
        exit()

    for collection in collections:

        coll_info = collection_info(collection, articlemeta_db)

        logger.info(u'Loading languages for %s', coll_info['domain'])
        logger.info(u'Using mode all_records %s', str(all_records))

        static_catalogs = StaticCatalog(coll_info['domain'])

        for document in load_documents(collection, articlemeta_db, 
                all_records=all_records):
            logger.debug(
                u'Checking fulltexts for %s_%s',
                collection,
                document.publisher_id
            )

            fulltexts = static_catalogs.fulltexts(document)

            if not isinstance(fulltexts, dict):
                logger.warning(
                    u'Document not loaded for %s_%s',
                    collection,
                    document.publisher_id
                )
                continue

            for key in fulltexts.keys():
                if not data_struct_regex.match(key):
                    logger.warning(
                        u'Document not loaded for %s_%s',
                        collection,
                        document.publisher_id
                    )
                    continue

            articlemeta_db['articles'].update(
                {'code': document.publisher_id, 'collection': document.collection_acronym},
                {'$set': static_catalogs.fulltexts(document)}
            )

            logger.debug(
                u'Update made for %s_%s',
                collection,
                document.publisher_id
            )


def main():
    db_dsn = os.environ.get('MONGODB_HOST', '127.0.0.1:27017')
    try:
        db_client = controller.get_dbconn(db_dsn)
    except:
        print('Fail to connect to:', db_dsn)
        sys.exit(1)
    else:
        articlemeta_db = controller.DataBroker(db_client).db

    parser = argparse.ArgumentParser(
        description="Load Languages from SciELO static files available in the file system"
    )

    _collections_acronyms = collections_acronym(articlemeta_db) 

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
        help='Apply processing to all records or just records without the languages parameter'
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

    collections = [args.collection] if args.collection else _collections_acronyms

    run(collections, articlemeta_db, args.all_records)


if __name__ == '__main__':
    main()

