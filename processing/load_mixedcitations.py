# coding: utf-8
"""
This scripts loads the mixed citations of a given article.
"""
import re
import os
import html
import argparse
import logging
import codecs
import json
import unicodedata
import sys


from articlemeta import controller
from xylose.scielodocument import Article

logger = logging.getLogger(__name__)
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
MONGODB_HOST = os.environ.get('MONGODB_HOST', 'mongodb://localhost:27017/articlemeta')

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

# if SENTRY_DSN:
#     # com raven (python < 3.7)
#     # LOGGING['handlers']['sentry'] = {
#     #     'level': 'ERROR',
#     #     'class': 'raven.handlers.logging.SentryHandler',
#     #     'dsn': SENTRY_DSN,
#     # }
#     # LOGGING['loggers']['']['handlers'].append('sentry')
#     sentry_sdk.init(
#         dsn=SENTRY_DSN,
#         integrations=[sentry_sdk.integrations.LoggingIntegration()]
#     )


try:
    articlemeta_db = controller.get_dbconn(MONGODB_HOST)
except:
    print('Fail to connect to:', MONGODB_HOST)
    sys.exit(1)


def remove_control_characters(data):
    return "".join(ch for ch in data if unicodedata.category(ch)[0] != "C")


def escape_html_http_tags(string):
    """Escapa trechos de uma string que podem ser interpretadas como tags HTML.

    >>> escape_html_http_tags("Citação disponível em <http://www.scielo.br>.")
    >>> "Citação disponível em &lt;http://www.scielo.br&gt;."
    >>> escape_html_http_tags("Citação disponível em <http://www.scielo.br")
    >>> "Citação disponível em &lt;http://www.scielo.br"
    """

    if "<http" not in string:
        return string

    match = re.compile(".*(<http.*?>|<http.*?>?).*", re.MULTILINE).match(string)

    if match:
        http_string = match.groups()[0]
        string = string.replace(http_string, html.escape(http_string))
    return string


def change_w_namespace(string):
    if 'w:st="on"' not in string:
        return string

    return string.replace('w:st="on"', 'w-st="on"')


def normalize_string(string):
    """Remove tags HTML, pontuação e espaços desnecessários.

    >>> normalize_string("<font>Mixed citation    <i>italic </i> :).</font>")
    >>> "Mixed citation "
    """

    string = re.sub(re.compile("<.*?>"), "", string)
    string = re.sub(r"\s+", " ", string)
    string = re.sub(r"[^\w\s]+", "", string, re.UNICODE)
    return string.strip()


def html_decode(string):
    string = escape_html_http_tags(string)
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

    check = html.unescape(mixed['mixed'].lower())
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
        _title = normalize_string(title).split(" ")
        _check = normalize_string(check)
        total_matches = 0

        for _str in _title:
            if _str in _check:
                total_matches += 1

        if (total_matches/len(_title)) >= 0.9:
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
            mixed["mixed"] = change_w_namespace(mixed['mixed'])
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


if __name__ == "__main__":
    main()