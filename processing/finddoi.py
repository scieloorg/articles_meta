# encoding: utf-8

import os
import json
import urlparse
import unicodedata
import logging
from difflib import SequenceMatcher
from ConfigParser import SafeConfigParser
import socket

import requests
from pymongo import MongoClient
from xylose.scielodocument import Article

from articlemeta import utils

CROSSREF_API_DOI = 'http://search.crossref.org/dois?'

config = utils.Configuration.from_file(os.environ.get('CONFIG_INI', os.path.dirname(__file__)+'/../config.ini'))
settings = dict(config.items())


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


def verify_doi(coins, article):

    found_doi = coins['doi'].replace(
        'http://dx.doi.org/', ''
    ).upper()

    # often the article ID is part of the DOI,
    # if that's the case, we found the right DOI
    if article.publisher_id.upper() in found_doi:
        # print 'id is part of DOI'
        return found_doi

    # most SciELO DOIs resolve to scielo.
    # check the resolved URL
    resolved_url = None
    try:
        logging.debug('Checking resolved SciELO URL for %s' % found_doi)
        resolved_url = requests.get(coins['doi'], timeout=3, allow_redirects=False).headers.get('location', '')
        logging.debug('Resolved SciELO URL is %s' % resolved_url)
    except requests.exceptions.Timeout, e:
        logging.error(e.message)
    except requests.exceptions.ConnectionError, e:
        logging.error(e.message)
    except requests.exceptions.HTTPError, e:
        logging.error(e.message)
    except requests.exceptions.InvalidSchema, e:
        logging.error(e.message)
    except socket.timeout, e:  # exception been catch just because: https://github.com/kennethreitz/requests/issues/1236
        logging.error(e.message)

    if resolved_url:
        qs = urlparse.parse_qs(urlparse.urlparse(resolved_url).query)  # grab the query string
        if article.publisher_id.upper() == qs.get('pid', [''])[0].upper():
            logging.debug('PID (%s) is part of the resolved URL %s' % (article.publisher_id.upper(), resolved_url))
            return found_doi
        elif 'scielo' in resolved_url:
            logging.debug('No matching PID (%s) for %s' % (article.publisher_id.upper(), resolved_url))
            return False

    coins = urlparse.parse_qs(str(coins))

    document = ' '.join([
        article.authors[0].get('given_names', '') if article.authors else '',
        article.authors[0].get('surname', '') if article.authors else '',
        article.original_title() or '',
        'publication_year: %s' % (article.publication_date[0:4] or ''),
        'volume: %s' % (article.volume or ''),
        'issue: %s' % (article.issue or '')
    ])

    request_document = ' '.join([
        coins.get('rft.aufirst', [''])[0],
        coins.get('rft.aulast', [''])[0],
        coins.get('rft.atitle', [''])[0],
        'publication_year: %s' % coins.get('rft.date', [''])[0],
        'volume: %s' % coins.get('rft.volume', [''])[0],
        'issue: %s' % coins.get('rft.issue', [''])[0],
    ]).decode('utf-8')

    if SequenceMatcher(None, document.lower(), request_document.lower()).ratio() >= float(settings['processing']['expected_ratio']):
        logging.debug(
            'Matching by %s ratio for strings (%s) and (%s)' % (
                settings['processing']['expected_ratio'],
                document,
                request_document
            )
        )
        return found_doi

    logging.debug(
        'No match found for (%s) and (%s)' % (
            document,
            request_document
        )
    )

    return False


def search_doi(article):
    data = {}
    data['q'] = ' '.join(
        [article.original_title() or '', article.journal.scielo_issn or '']
    ).encode('utf-8')
    data['year'] = article.publication_date[0:4]

    response = None
    try:
        response = requests.get(
            CROSSREF_API_DOI,
            params=data,
            timeout=3
        )
    except requests.exceptions.Timeout, e:
        logging.error(e.message)
    except requests.exceptions.ConnectionError, e:
        logging.error(e.message)
    except requests.exceptions.HTTPError, e:
        logging.error(e.message)
    except socket.timeout, e:  # exception been catch just because: https://github.com/kennethreitz/requests/issues/1236
        logging.error(e.message)

    try:
        response = response.json()
    except ValueError:
        response = None
        logging.error(e.message)
    except AttributeError:
        response = None
        logging.error(e.message)

    if not response:
        return None

    if len(response) == 0:
        return None

    if verify_doi(response[0], article):
        return response[0].get('doi', '')


def load_articles_doi_from_crossref(mongo_uri=settings['app']['mongo_uri']):
    logging.info('Findind and registering DOIs for SciELO articles')
    try:
        coll = MongoClient(mongo_uri)['scielo_network']['articles']
        logging.debug('Connecting to MongoDB database at %s' % mongo_uri)
    except:
        logging.error('Failing to MongoDB database at %s' % mongo_uri)

    regs = coll.find({'article.doi': {'$exists': 0}}, {'code': 1, 'collection': 1})

    for code, collection in [[i['code'], i['collection']] for i in regs]:
        article = Article(coll.find_one({'code': code, 'collection': collection}, {'citations': 0, '_id': 0}))
        logging.debug('Finding DOI for (%s)' % code)

        doi = search_doi(article)

        if doi:
            coll.update({'code': code, 'collection': collection}, {'$set': {'article.doi': doi}})
            logging.debug('DOI (%s) Registered for (%s)' % (doi.upper().replace('HTTP://DX.DOI.ORG/',''), code))


def load_citations_doi_from_crossref(mongo_uri=settings['app']['mongo_uri']):
    logging.info('Findind and registering DOIs for SciELO article citations')
    pass


if __name__ == "__main__":
    _config_logging(settings['logging']['level'], settings['logging']['file'])

    load_articles_doi_from_crossref()
