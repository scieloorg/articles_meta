# coding: utf-8
import json
import argparse
import logging
import os
import sys

import thriftpy
from thriftpy.thrift import TProcessor

from articlemeta.controller import DataBroker
from articlemeta import utils
from xylose.scielodocument import Article


logger = logging.getLogger(__name__)

articlemeta_thrift = thriftpy.load(
    os.path.dirname(__file__)+'/articlemeta.thrift',
    module_name='articlemeta_thrift'
)


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

    def article_history_changes(self, collection, event, code, from_date, until_date, limit, offset):

        from_date = from_date or '1500-01-01'
        limit = limit or 1000
        offset = offset or 0

        try:
            data = self._databroker.historychanges(
                document_type= 'article',
                collection=collection,
                event=event,
                code=code,
                from_date=from_date,
                until_date=until_date,
                limit=limit,
                offset=offset
            )
        except:
            articlemeta_thrift.ServerError('Server error: DataBroker.historychanges')

        
        objs = [articlemeta_thrift.event_document(code=i['code'], collection=i['collection'], event=i['event'], date=i['date']) for i in data['objects']]

        return objs

    def get_article_identifiers(self, collection, from_date, until_date, limit, offset):

        from_date = from_date or '1500-01-01'
        limit = limit or 1000
        offset = offset or 0

        try:
            data = self._databroker.identifiers_article(
                collection=collection,
                from_date=from_date,
                until_date=until_date,
                limit=limit,
                offset=offset
            )
        except:
            articlemeta_thrift.ServerError('Server error: DataBroker.identifiers_article')

        
        objs = [articlemeta_thrift.article_identifiers(code=i['code'], collection=i['collection'], processing_date=i['processing_date']) for i in data['objects']]

        return objs


    def get_article(self, code, collection, replace_journal_metadata):

        try:
            data = self._databroker.get_article(code, collection=collection, replace_journal_metadata=replace_journal_metadata)
        except:
            articlemeta_thrift.ServerError('Server error: DataBroker.get_article')

        return json.dumps(data)

    def journal_history_changes(self, collection, event, code, from_date, until_date, limit, offset):

        from_date = from_date or '1500-01-01'
        limit = limit or 1000
        offset = offset or 0

        try:
            data = self._databroker.historychanges(
                document_type= 'journal',
                collection=collection,
                event=event,
                code=code,
                from_date=from_date,
                until_date=until_date,
                limit=limit,
                offset=offset
            )
        except:
            articlemeta_thrift.ServerError('Server error: DataBroker.historychanges')

        objs = [articlemeta_thrift.event_journal(code=i['code'], collection=i['collection'], event=i['event'], date=i['date']) for i in data['objects']]

        return objs

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

app = TProcessor(articlemeta_thrift.ArticleMeta, Dispatcher())
