# coding: utf-8
import json
import logging
import os

import thriftpywrap
import thriftpy

from articlemeta.controller import DataBroker
from articlemeta import utils
from articlemeta.export import Export
from xylose.scielodocument import Article

logger = logging.getLogger(__name__)

articlemeta_thrift = thriftpy.load(
    os.path.join(os.path.dirname(__file__), 'articlemeta.thrift'))


class Dispatcher(object):
    def __init__(self):
        config = utils.Configuration.from_env()
        settings = dict(config.items())

        self._databroker = DataBroker.from_dsn(
            settings['app:main']['mongo_uri'],
            reuse_dbconn=True)

    def get_collection_identifiers(self):
        try:
            data = self._databroker.identifiers_collection()
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.identifiers_collection')

        return [articlemeta_thrift.collection(i['code'], i['acron'],
            i['acron2'], i['status'], i['domain'], i['original_name'],
            i['has_analytics']) for i in data]

    def get_collection(self, code):

        try:
            data = self._databroker.get_collection(code)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.get_collection')

        return articlemeta_thrift.collection(data['code'], data['acron'],
                                             data['acron2'], data['status'],
                                             data['domain'], data['original_name'],
                                             data['has_analytics'])

    def article_history_changes(self, collection, event, code, from_date,
                                until_date, limit, offset):

        from_date = from_date or '1500-01-01'
        limit = limit or 1000
        offset = offset or 0

        try:
            data = self._databroker.historychanges(document_type='article',
                                                   collection=collection,
                                                   event=event,
                                                   code=code,
                                                   from_date=from_date,
                                                   until_date=until_date,
                                                   limit=limit,
                                                   offset=offset)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.historychanges')

        objs = [articlemeta_thrift.event_document(code=i['code'],
                                                  collection=i['collection'],
                                                  event=i['event'],
                                                  date=i['date'])
                for i in data['objects']]

        return objs

    def get_article_identifiers(self, collection, issn, from_date, until_date,
                                limit, offset):

        from_date = from_date or '1500-01-01'
        limit = limit or 1000
        offset = offset or 0

        try:
            data = self._databroker.identifiers_article(collection=collection,
                                                        issn=issn,
                                                        from_date=from_date,
                                                        until_date=until_date,
                                                        limit=limit,
                                                        offset=offset)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.identifiers_article')

        objs = [articlemeta_thrift.article_identifiers(
            code=i['code'],
            collection=i['collection'],
            processing_date=i['processing_date']) for i in data['objects']]

        return objs

    def get_article(self, code, collection, replace_journal_metadata, fmt):

        try:
            data = self._databroker.get_article(
                code,
                collection=collection,
                replace_journal_metadata=replace_journal_metadata
            )
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.get_article')

        if data:
            if fmt == 'xmlwos':
                return Export(data).pipeline_sci()

            if fmt == 'xmldoaj':
                return Export(data).pipeline_doaj()

            if fmt == 'xmlrsps':
                return Export(data).pipeline_rsps()

            if fmt == 'xmlpubmed':
                return Export(data).pipeline_pubmed()

        return json.dumps(data)

    def journal_history_changes(self, collection, event, code, from_date,
                                until_date, limit, offset):

        from_date = from_date or '1500-01-01'
        limit = limit or 1000
        offset = offset or 0

        try:
            data = self._databroker.historychanges(document_type='journal',
                                                   collection=collection,
                                                   event=event,
                                                   code=code,
                                                   from_date=from_date,
                                                   until_date=until_date,
                                                   limit=limit,
                                                   offset=offset)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.historychanges')

        objs = [articlemeta_thrift.event_journal(code=i['code'],
                                                 collection=i['collection'],
                                                 event=i['event'],
                                                 date=i['date'])
                for i in data['objects']]

        return objs

    def get_journal_identifiers(self, collection, limit, offset):

        limit = limit or 0
        offset = offset or 0

        try:
            data = self._databroker.identifiers_journal(collection=collection,
                                                        limit=limit,
                                                        offset=offset)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.identifiers_journal')

        objs = [
            articlemeta_thrift.journal_identifiers(code=i['code'],
                                                   collection=i['collection'])
            for i in data['objects'] if i['code'][0] != None
        ]

        return objs

    def get_journal(self, code, collection):

        try:
            data = self._databroker.get_journal(collection=collection,
                                                issn=code)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.get_journal')

        if isinstance(data, list):
            return json.dumps(data[0])

        return json.dumps(data)

    def set_doaj_id(self, code, collection, doaj_id):
        try:
            self._databroker.set_doaj_id(code, collection, doaj_id)
            return True
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.set_doaj_id')

        return False

    def set_aid(self, code, collection, aid):
        try:
            self._databroker.set_aid(code, collection, aid)
            return True
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.set_aid')

        return False

    def exists_article(self, code, collection):
        try:
            return self._databroker.exists_article(code, collection)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.exists_article')

        return False

main = thriftpywrap.ConsoleApp(articlemeta_thrift.ArticleMeta, Dispatcher)
