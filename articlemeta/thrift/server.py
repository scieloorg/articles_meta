# coding: utf-8
import json
import logging
import os
import uuid

import thriftpywrap
import thriftpy

from articlemeta.controller import DataBroker, get_dbconn
from articlemeta import utils
from articlemeta.export import Export

logger = logging.getLogger(__name__)

SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
MONGODB_HOST = os.environ.get('MONGODB_HOST', None)

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
        'publication.thrift.server': {
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

articlemeta_thrift = thriftpy.load(
    os.path.join(os.path.dirname(__file__), 'articlemeta.thrift'))


class Dispatcher(object):
    def __init__(self):
        config = utils.Configuration.from_env()
        settings = dict(config.items())

        db_dsn = os.environ.get('MONGODB_HOST', settings.get('mongo_uri', '127.0.0.1:27017'))

        self._admintoken = os.environ.get('ADMIN_TOKEN', None) or settings['app:main'].get('admintoken', uuid.uuid4().hex)

        db_client = get_dbconn(db_dsn)
        self._databroker = DataBroker(db_client)

    def getInterfaceVersion(self):
        return articlemeta_thrift.VERSION

    def get_collection_identifiers(self):
        try:
            data = self._databroker.identifiers_collection()
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.identifiers_collection')

        return [articlemeta_thrift.collection(i['code'], i['acron'],
            i.get('acron2', ''), i.get('status', ''), i['domain'], i['original_name'],
            i['has_analytics'], i.get('is_active', False), i.get('type', '')) for i in data]

    def get_collection(self, code):

        logger.debug('AM Thrift - get_collection(code=%s)' % code)
        try:
            data = self._databroker.get_collection(code)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.get_collection')

        if not data:
            raise articlemeta_thrift.ValueError(
                'Value error: no collection %s' % code)

        return articlemeta_thrift.collection(data['code'], data['acron'],
                                             data.get('acron2', ''), data.get('status', ''),
                                             data['domain'], data['original_name'],
                                             data['has_analytics'],
                                             data.get('is_active', False), data.get('type', ''))

    def article_history_changes(self, collection, event, code, from_date,
                                until_date, limit, offset):

        logger.debug(
            'AM Thrift - article_history_changes('
            'collection=%s,event=%s,code=%s,from_date=%s,'
            'until_date=%s,limit=%s,offset=%s)'
            % (collection, event, code, from_date, until_date, limit, offset)
        )

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

    def issue_history_changes(self, collection, event, code, from_date,
                              until_date, limit, offset):

        logger.debug(
            'AM Thrift - issue_history_changes('
            'collection=%s,event=%s,code=%s,from_date=%s,'
            'until_date=%s,limit=%s,offset=%s)'
            % (collection, event, code, from_date, until_date, limit, offset)
        )

        from_date = from_date or '1500-01-01'
        limit = limit or 1000
        offset = offset or 0

        try:
            data = self._databroker.historychanges(
                document_type='issue',
                collection=collection,
                event=event,
                code=code,
                from_date=from_date,
                until_date=until_date,
                limit=limit,
                offset=offset
            )
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.historychanges')

        objs = [articlemeta_thrift.event_issue(
            code=i['code'],
            collection=i['collection'],
            event=i['event'],
            date=i['date']
        ) for i in data['objects']]

        return objs

    def get_articles(
        self, collection, issn, from_date, until_date,
        limit, offset, extra_filter=None, replace_journal_metadata=False,
        body=False
    ):

        logger.debug(
            'AM Thrift - get_articles('
            'collection=%s,issn=%s,from_date=%s,until_date=%s,limit=%s,'
            'offset=%s,extra_filter=%s,replace_journal_metadata=%s,body=%s)'
            % (collection, issn, from_date, until_date, limit, offset,
                extra_filter, replace_journal_metadata, body)
        )

        from_date = from_date or '1500-01-01'
        limit = limit or 100
        offset = offset or 0

        try:
            data = self._databroker.get_articles_full(
                collection=collection,
                issn=issn,
                from_date=from_date,
                until_date=until_date,
                limit=limit,
                offset=offset,
                extra_filter=extra_filter,
                replace_journal_metadata=False,
                body=False
            )
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.get_articles')

        return json.dumps(data)

    def get_article_identifiers(self, collection, issn, from_date, until_date,
                                limit, offset, extra_filter=None):

        logger.debug(
            'AM Thrift - get_article_identifiers('
            'collection=%s,issn=%s,from_date=%s,until_date=%s,limit=%s,'
            'offset=%s,extra_filter=%s)'
            % (collection, issn, from_date, until_date, limit, offset, extra_filter)
        )

        from_date = from_date or '1500-01-01'
        limit = limit or 1000
        offset = offset or 0

        try:
            data = self._databroker.identifiers_article(
                collection=collection,
                issn=issn,
                from_date=from_date,
                until_date=until_date,
                limit=limit,
                offset=offset,
                extra_filter=extra_filter
            )
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.identifiers_article')

        objs = [articlemeta_thrift.article_identifiers(
            code=i['code'],
            collection=i['collection'],
            processing_date=i['processing_date'],
            aid=i.get('aid', ''),
            doi=i.get('doi', '')) for i in data['objects']]

        return objs

    def get_issues(
        self, collection, issn, from_date, until_date,
        limit, offset, extra_filter=None
    ):

        logger.debug(
            'AM Thrift - get_issues('
            'collection=%s,issn=%s,from_date=%s,until_date=%s,limit=%s,'
            'offset=%s,extra_filter=%s)'
            % (collection, issn, from_date, until_date, limit, offset, extra_filter)
        )

        from_date = from_date or '1500-01-01'
        limit = limit or 100
        offset = offset or 0

        try:
            data = self._databroker.get_issues_full(
                collection=collection,
                issn=issn,
                from_date=from_date,
                until_date=until_date,
                limit=limit,
                offset=offset,
                extra_filter=extra_filter
            )
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.get_issues')

        return json.dumps(data)

    def get_issue_identifiers(self, collection, issn, from_date, until_date,
                                limit, offset, extra_filter=None):

        logger.debug(
            'AM Thrift - get_issue_identifiers('
            'collection=%s,issn=%s,from_date=%s,until_date=%s,limit=%s,'
            'offset=%s,extra_filter=%s)'
            % (collection, issn, from_date, until_date, limit, offset, extra_filter)
        )

        from_date = from_date or '1500-01-01'
        limit = limit or 1000
        offset = offset or 0

        try:
            data = self._databroker.identifiers_issue(
                collection=collection,
                issn=issn,
                from_date=from_date,
                until_date=until_date,
                limit=limit,
                offset=offset,
                extra_filter=extra_filter
            )
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.identifiers_issue')

        objs = [articlemeta_thrift.issue_identifiers(
            code=i['code'],
            collection=i['collection'],
            processing_date=i['processing_date']) for i in data['objects']]

        return objs

    def delete_journal(self, code, collection, admintoken):

        logger.debug(
            'AM Thrift - delete_journal(code=%s,collection=%s)'
            % (code, collection)
        )

        if admintoken != self._admintoken:
            raise articlemeta_thrift.Unauthorized(
                'Unautorized Access: Invalid admin token')

        try:
            result = self._databroker.delete_journal(code, collection=collection)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.delete_journal')

        try:
            return json.dumps(result)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.delete_journal')

    def delete_issue(self, code, collection, admintoken):

        logger.debug(
            'AM Thrift - delete_issue(code=%s,collection%s)'
            % (code, collection)
        )

        if admintoken != self._admintoken:
            raise articlemeta_thrift.Unauthorized(
                'Unautorized Access: Invalid admin token')

        try:
            result = self._databroker.delete_issue(code, collection=collection)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.delete_issue')

        try:
            return json.dumps(result)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.delete_journal')

    def delete_article(self, code, collection, admintoken):

        logger.debug(
            'AM Thrift - delete_article(code=%s,collection%s)'
            % (code, collection)
        )

        if admintoken != self._admintoken:
            raise articlemeta_thrift.Unauthorized(
                'Unautorized Access: Invalid admin token')

        try:
            result = self._databroker.delete_article(code, collection=collection)
        except Exception as e:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.delete_article %s' % str(e))

        try:
            return json.dumps(result)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.delete_journal')

    def add_journal(self, metadata, admintoken):
        logger.debug(
            'AM Thrift - add_journal(metadata=%s)' % metadata
        )

        if admintoken != self._admintoken:
            raise articlemeta_thrift.Unauthorized(
                'Unautorized Access: Invalid admin token')

        jdata = None
        try:
            jdata = json.loads(metadata)
        except:
            raise articlemeta_thrift.ValueError(
                'Value error: DataBroker.add_journal, Invalid JSON')

        data = None
        try:
            data = self._databroker.add_journal(jdata)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.add_journal')

        if data:
            return json.dumps(data)

        raise articlemeta_thrift.ServerError(
            'Server error: DataBroker.add_journal, Nondata inserted')

    def add_article(self, metadata, admintoken):
        logger.debug(
            'AM Thrift - add_article(metadata=%s)' % metadata
        )

        if admintoken != self._admintoken:
            raise articlemeta_thrift.Unauthorized(
                'Unautorized Access: Invalid admin token')

        jdata = None
        try:
            jdata = json.loads(metadata)
        except:
            raise articlemeta_thrift.ValueError(
                'Value error: DataBroker.add_article, Invalid JSON')

        data = None
        try:
            data = self._databroker.add_article(jdata)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.add_article')

        if data:
            return json.dumps(data)

        raise articlemeta_thrift.ServerError(
            'Server error: DataBroker.add_article, Nondata inserted')

    def add_issue(self, metadata, admintoken):
        logger.debug(
            'AM Thrift - add_issue(metadata=%s)' % metadata
        )

        if admintoken != self._admintoken:
            raise articlemeta_thrift.Unauthorized(
                'Unautorized Access: Invalid admin token')

        jdata = None
        try:
            jdata = json.loads(metadata)
        except:
            raise articlemeta_thrift.ValueError(
                'Value error: DataBroker.add_issue, Invalid JSON')

        data = None
        try:
            data = self._databroker.add_issue(jdata)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.add_issue')

        if data:
            return json.dumps(data)

        raise articlemeta_thrift.ServerError(
            'Server error: DataBroker.add_issue, Nondata inserted')

    def get_article(self, code, collection, replace_journal_metadata, fmt, body=False):

        logger.debug(
            'AM Thrift - get_article('
            'code=%s,collection=%s,replace_journal_metadata=%s,fmt=%s,body=%s)'
            % (code, collection, replace_journal_metadata, fmt, body)
        )

        try:
            data = self._databroker.get_article(
                code,
                collection=collection,
                replace_journal_metadata=replace_journal_metadata,
                body=body
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

            if fmt == 'xmlcrossref':
                return Export(data).pipeline_crossref(
                    self._databroker.is_name_suffix)

            if fmt == 'opac':
                return json.dumps(Export(data).pipeline_opac())

        return json.dumps(data)

    def get_issue(self, code, collection, replace_journal_metadata):

        logger.debug(
            'AM Thrift - get_issue(code=%s,collection=%s,replace_journal_metadata=%s)'
            % (code, collection, replace_journal_metadata)
        )

        try:
            data = self._databroker.get_issue(
                code,
                collection=collection,
                replace_journal_metadata=replace_journal_metadata
            )
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.get_issue')

        return json.dumps(data)

    def journal_history_changes(self, collection, event=None, code=None, from_date=None,
                                until_date=None, limit=None, offset=None):

        logger.debug(
            'AM Thrift - journal_history_changes('
            'collection=%s,event=%s,code=%s,from_date=%s,'
            'until_date=%s,limit=%s,offset=%s)'
            % collection
        )

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

    def get_journal_identifiers(self, collection, issn=None, limit=None, offset=None, extra_filter=None):

        logger.debug(
            'AM Thrift - get_journal_identifiers('
            'collection=%s,issn=%s,limit=%s,offset=%s,extra_filter=%s)'
            % (collection, issn, limit, offset, extra_filter)
        )

        limit = limit or 0
        offset = offset or 0

        try:
            data = self._databroker.identifiers_journal(collection=collection,
                                                        issn=issn,
                                                        limit=limit,
                                                        offset=offset,
                                                        extra_filter=extra_filter)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.identifiers_journal')

        objs = [
            articlemeta_thrift.journal_identifiers(
                code=i['code'],
                collection=i['collection'],
                processing_date=i['processing_date']) for i in data['objects'] if i['code']
            ]

        return objs

    def get_journal(self, code, collection):

        logger.debug(
            'AM Thrift - get_journal(code=%s,collection=%s)' % (code, collection)
        )

        try:
            data = self._databroker.get_journal(collection=collection,
                                                issn=code)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.get_journal')

        if isinstance(data, list):
            return json.dumps(data[0]) if data else ''

        return json.dumps(data)

    def set_doaj_id(self, code, collection, doaj_id, admintoken):
        logger.debug(
            'AM Thrift - set_doaj_id(code=%s,collection=%s,doaj_id=%s)'
            % (code, collection, doaj_id)
        )

        if admintoken != self._admintoken:
            raise articlemeta_thrift.Unauthorized(
                'Unautorized Access: Invalid admin token')

        try:
            self._databroker.set_doaj_id(code, collection, doaj_id)
            return True
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.set_doaj_id')

        return False

    def set_aid(self, code, collection, aid, admintoken):
        logger.debug(
            'AM Thrift - set_aid(code=%s,collection=%s,aid=%s)'
            % (code, collection, aid)
        )

        if admintoken != self._admintoken:
            raise articlemeta_thrift.Unauthorized(
                'Unautorized Access: Invalid admin token')

        try:
            self._databroker.set_aid(code, collection, aid)
            return True
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.set_aid')

        return False

    def exists_article(self, code, collection):
        logger.debug(
            'AM Thrift - exists_article(code=%s,collection=%s)' % (code, collection)
        )

        try:
            return self._databroker.exists_article(code, collection)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.exists_article')

        return False

    def exists_issue(self, code, collection):
        logger.debug(
            'AM Thrift - exists_issue(code=%s,collection=%s)' % (code, collection)
        )

        try:
            return self._databroker.exists_issue(code, collection)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.exists_issue')

        return False

    def exists_journal(self, code, collection):
        logger.debug(
            'AM Thrift - exists_journal(code=%s,collection=%s)' % (code, collection)
        )

        try:
            return self._databroker.exists_journal(code, collection)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.exists_journal')

        return False

    def get_issue_code_from_label(self, label, journal_code, collection):
        logger.debug(
            'AM Thrift - get_issue_code_from_label(label=%s,journal_code=%s,collection=%s)'
            % (label, journal_code, collection)
        )

        try:
            return self._databroker.get_issue_code_from_label(label,
                    journal_code, collection)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.get_issue_code_from_label')

    def is_name_suffix(self, suffix):
        logger.debug(
            'AM Thrift - is_name_suffix(suffix=%s)' % suffix
        )

        try:
            return self._databroker.is_name_suffix(suffix)
        except:
            raise articlemeta_thrift.ServerError(
                'Server error: DataBroker.is_name_suffix')

        return False

    def add_name_suffix(self, metadata, admintoken):
        logger.debug(
            'AM Thrift - add_name_suffix(metadata=%s)' % metadata
        )
        if admintoken != self._admintoken:
            raise articlemeta_thrift.Unauthorized(
                'Unautorized Access: Invalid admin token')
        try:
            jdata = json.loads(metadata)
        except:
            raise articlemeta_thrift.ValueError(
                'Value error: DataBroker.add_name_suffix, Invalid JSON')
        else:
            try:
                self._databroker.add_name_suffix(jdata)
            except:
                raise articlemeta_thrift.ServerError(
                    'Server error: DataBroker.add_name_suffix, Nondata inserted')


main = thriftpywrap.ConsoleApp(articlemeta_thrift.ArticleMeta, Dispatcher)
