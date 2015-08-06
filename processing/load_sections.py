# coding: utf-8
"""
This scripts loads the issue section whiting a given article.
The lists of Sections must be given and respect the following format.
"collection acronym","language","code","text"
"""
from datetime import datetime, timedelta
import argparse
import logging
import re
import os
import requests

from pymongo import MongoClient
from articlemeta import utils
from xylose.scielodocument import Article

logger = logging.getLogger(__name__)

FROM = datetime.now() - timedelta(days=15)
FROM.isoformat()[:10]

file_regex = re.compile(r'serial.*.htm|.*.xml')
data_struct_regex = re.compile(r'^fulltexts\.(pdf|html)\.[a-z][a-z]$')

config = utils.Configuration.from_env()
settings = dict(config.items())

try:
    articlemeta_db = MongoClient(settings['app:main']['mongo_uri'])['articlemeta']
except:
    logging.error('Fail to connect to (%s)' % settings['app:main']['mongo_uri'])

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

def collections_acronym():

    collections = articlemeta_db['collections'].find({}, {'_id': 0})

    return [i['code'] for i in collections]

def collection_info(collection):

    info = articlemeta_db['collections'].find_one({'acron': collection}, {'_id': 0})

    return info

def do_request(url, json=True):


    headers = {
        'User-Agent': 'SciELO Processing ArticleMeta: LoadSection'
    }

    try:
        document = requests.get(url, headers=headers)
    except:
        logger.error(u'HTTP request error for: %s' % url)
    else:
        if json:
            return document.json()
        else:
            return document

def load_documents(collection, all_records=False):

    fltr = {
        'collection': collection
    }

    if all_records == False:
        fltr['section'] = {'$exists': 0}

    documents = articlemeta_db['articles'].find(
        fltr,
        {'_id': 0, 'citations': 0},
        no_cursor_timeout=True
    )

    for document in documents:
        yield Article(document)

    documents.close()

class StaticCatalog(object):

    def __init__(self, collection):
        self.catalog = self._load_static_catalog(collection, 'section')

    def _load_static_catalog(self, source, type):
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

        logger.info(u'Loading static_%s_catalog.txt from server %s' % (type, source))

        filename = 'static_%s_catalog.txt' % type

        url = '/'.join(['http:/', source, filename])
        content = do_request(url, json=False).iter_lines()

        items = set([i.decode('iso-8859-1') for i in content])

        sections = {}
        for line in sorted(items):
            splited_line = [i.strip() for i in line.split('|')]
            if len(splited_line) != 5:
                continue
            collection = splited_line[0]
            issue = splited_line[1]
            language = splited_line[2]
            code = splited_line[3]
            label = splited_line[4]

            sections.setdefault(collection, {})
            sections[collection].setdefault(issue, {})
            sections[collection][issue].setdefault(code, {})
            sections[collection][issue][code].update({language: label})
        
        return sections

    def get_section_available(self, pid, collection, issue, section_code):
        """
        This method checks the existence of the section agains the catalog.
        collection: scl <acronym 3 letters>
        issue: 1690-751520090003 <PID SciELO for issues>
        code: ENL010 <section legacy code>
        """
        logger.debug(u'Checking sessions in {0}, {1}, {2} for {3}'.format(
            collection,
            issue,
            section_code,
            pid)
        )

        try:
            section = self.catalog[collection][issue][section_code]
        except:
            logger.warning(u'Session not found int catalog for {0}, {1}, {2} for {3}'.format(
                collection,
                issue,
                section_code,
                pid)
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
        collection = document.collection_acronym
        section_code = document.section_code

        section = self.get_section_available(pid, collection, issue_pid, section_code)

        if not section:
            return None

        return section
            

def run(collections, all_records=False):

    if not isinstance(collections, list):
        logger.error('Collections must be a list of collection acronym')
        exit()

    for collection in collections:

        coll_info = collection_info(collection)

        logger.info(u'Loading sections for %s' % coll_info['domain'])
        logger.info(u'Using mode all_records %s' % str(all_records))

        static_catalogs = StaticCatalog('www.scielo.br')

        for document in load_documents(collection, all_records=all_records):
            logger.debug(u'Checking section for %s_%s' % (
                collection,
                document.publisher_id
            ))

            section = static_catalogs.section(document)

            if not isinstance(section, dict):
                logger.warning(u'Section not loaded for %s_%s' % (
                    collection,
                    document.publisher_id
                ))
                continue

            articlemeta_db['articles'].update(
                {'code': document.publisher_id,'collection': document.collection_acronym}, 
                {'$set': {'section': section}}
            )

            logger.debug(u'Update made for %s_%s' % (
                collection,
                document.publisher_id
            ))

def main():
    parser = argparse.ArgumentParser(
        description="Load Languages from SciELO static files available in the file system"
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

    collections = [args.collection] if args.collection else collections_acronym()

    run(collections, args.all_records)
