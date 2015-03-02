# coding: utf-8
import json
import argparse
import logging
import os
import sys

import thriftpy
from thriftpy.rpc import make_server

from articlemeta.controller import DataBroker
from articlemeta import utils
from xylose.scielodocument import Article

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = '11720'

articlemeta_thrift = thriftpy.load(
    os.path.dirname(__file__)+'/articlemeta.thrift',
    module_name='articlemeta_thrift'
)

def _config_logging(logging_level='INFO', logging_file=None):

    allowed_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger('rpc_articlemeta')
    logger.setLevel(allowed_levels.get(logging_level, 'INFO'))

    if logging_file:
        hl = logging.FileHandler(logging_file, mode='a')
    else:
        hl = logging.StreamHandler()

    hl.setFormatter(formatter)
    hl.setLevel(allowed_levels.get(logging_level, 'INFO'))

    logger.addHandler(hl)

    return logger


class Dispatcher(object):

    def __init__(self):

        config = utils.Configuration.from_file(os.environ.get(
            'CONFIG_INI',
            os.path.dirname(__file__)+'/../../config.ini')
        )
        settings = dict(config.items())

        self._databroker = DataBroker.from_dsn(settings['app:main']['mongo_uri'], reuse_dbconn=True)

    def get_collection_identifiers(self):

        try:
            data = self._databroker.identifiers_collection()
        except:
            articlemeta_thrift.ServerError('Server error: DataBroker.identifiers_collection')


        return [articlemeta_thrift.collection(i['code'],i['acron'],i['acron2'],i['status'],i['domain']) for i in data]

    def get_collection(self, code):

        try:
            data = self._databroker.get_collection(code)
        except:
            articlemeta_thrift.ServerError('Server error: DataBroker.get_collection')

        return articlemeta_thrift.collection(
            data['code'],
            data['acron'],
            data['acron2'],
            data['status'],
            data['domain']
        )

    def get_article_identifiers(self, collection, from_date, until_date, limit, offset):

        from_date = from_date or '1500-01-01'
        limit = limit or 0
        offset = offset or 0

        data = self._databroker.identifiers_article(
            collection=collection,
            from_date=from_date,
            until_date=until_date,
            limit=limit,
            offset=offset
        )

        try:
            objs = [articlemeta_thrift.article_identifiers(code=i['code'], collection=i['collection'], processing_date=i['processing_date']) for i in data['objects']]
        except:
            articlemeta_thrift.ServerError('Server error: DataBroker.identifiers_article')

        return objs


    def get_article(self, code, collection, replace_journal_metadata):

        try:
            data = self._databroker.get_article(code, collection=collection, replace_journal_metadata=replace_journal_metadata)
        except:
            articlemeta_thrift.ServerError('Server error: DataBroker.get_article')

        return json.dumps(data)

    def get_journal_identifiers(self, collection, limit, offset):

        limit = limit or 0
        offset = offset or 0

        try:
            data = self._databroker.identifiers_journal(collection=collection, limit=limit, offset=offset)
        except:
            articlemeta_thrift.ServerError('Server error: DataBroker.identifiers_journal')

        objs = [articlemeta_thrift.journal_identifiers(code=i['code'], collection=i['collection']) for i in data['objects'] if i['code'][0] != None]

        return objs

    def get_journal(self, code, collection):

        try:
            data = self._databroker.get_journal(collection=collection, issn=code)
        except:
            articlemeta_thrift.ServerError('Server error: DataBroker.get_journal')

        if isinstance(data, list):
            return json.dumps(data[0])

        return json.dumps(data)

def main(host=DEFAULT_HOST, port=DEFAULT_PORT):

    server = make_server(
        articlemeta_thrift.ArticleMeta,
        Dispatcher(),
        host,
        port
    )

    logger.info('Starting Server on %s:%s' % (host, port))

    server.serve()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="RPC Server for Article Meta"
    )

    parser.add_argument(
        '--host',
        '-i',
        default=DEFAULT_HOST,
        help='RPC Server host'
    )

    parser.add_argument(
        '--port',
        '-p',
        default=DEFAULT_PORT,
        help='RPC Server port'
    )

    parser.add_argument(
        '--logging_file',
        '-o',
        default='/var/log/rpc_articlemeta.log',
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

    logger = _config_logging(args.logging_level, args.logging_file)

    main(
        host=args.host,
        port=args.port
    )