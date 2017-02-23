# coding: utf-8
from urllib.parse import urlparse
import warnings
import json

import pymongo
from xylose.scielodocument import Article, Journal, Issue
from articlemeta.decorators import LogHistoryChange
from datetime import datetime

LIMIT = 1000


def get_dbconn(db_dsn):
    """Connects to the MongoDB server and returns a database handler."""

    def _ensure_indexes(db):
        """
        Ensures that an index exists on specified collections.

        Definitions:
        index_by_collection = {
            'collection_name': [
                ('field_name_1', pymongo.DESCENDING),
                ('field_name_2', pymongo.ASCENDING),
                ...
            ],
        }

        Obs:
        Care must be taken when the database is being accessed through multiple clients at once.
        If an index is created using this client and deleted using another,
        any call to ensure_index() within the cache window will fail to re-create the missing index.

        Docs:
        http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.ensure_index
        """
        index_by_collection = {
            'historychanges_article': [
                ('date', pymongo.ASCENDING),
                ('collection', pymongo.ASCENDING),
                ('code', pymongo.ASCENDING),
            ],
            'historychanges_journal': [
                ('date', pymongo.ASCENDING),
                ('collection', pymongo.ASCENDING),
                ('code', pymongo.ASCENDING),
            ],
        }

        for collection, indexes in index_by_collection.items():
            db[collection].ensure_index(indexes)

    db_url = urlparse(db_dsn)
    conn = pymongo.MongoClient(host=db_url.hostname, port=db_url.port)
    db = conn[db_url.path[1:]]
    if db_url.username and db_url.password:
        db.authenticate(db_url.username, db_url.password)
    _ensure_indexes(db)
    return db


class DataBroker(object):
    _dbconn_cache = {}

    def __init__(self, databroker):
        self.db = databroker

    @classmethod
    def from_dsn(cls, db_dsn, reuse_dbconn=False):
        """Returns a DataBroker instance for a given DSN.

        :param db_dsn: Domain Service Name, i.e. mongodb://192.168.1.162:27017/scielo_network
        :reuse_dbconn: (optional) If connections to MongoDB must be reused
        """
        if reuse_dbconn:
            cached_db = cls._dbconn_cache.get(db_dsn)
            if cached_db is None:
                db = get_dbconn(db_dsn)
                cls._dbconn_cache[db_dsn] = db
            else:
                db = cached_db
        else:
            db = get_dbconn(db_dsn)

        return cls(db)

    def _check_article_meta(self, metadata):
        """
            This method will check the given metadata and retrieve
            a new dictionary with some new fields.
        """

        article = Article(metadata)

        issns = set(
            [
                article.journal.any_issn(priority=u'electronic'),
                article.journal.any_issn(priority=u'print'),
                article.journal.scielo_issn
            ]
        )

        metadata['code'] = article.publisher_id
        metadata['code_issue'] = article.publisher_id[1:18]
        metadata['code_title'] = list(issns)
        metadata['collection'] = article.collection_acronym
        metadata['document_type'] = article.document_type
        metadata['publication_year'] = article.publication_date[0:4]
        metadata['publication_date'] = article.publication_date
        metadata['validated_scielo'] = 'False'
        metadata['validated_wos'] = 'False'
        metadata['sent_wos'] = 'False'
        metadata['applicable'] = 'False'
        metadata['version'] = article.data_model_version

        if article.doi:
            metadata['doi'] = article.doi.upper()

        try:
            metadata['processing_date'] = article.processing_date
        except:
            metadata['processing_date'] = datetime.now().date().isoformat()

        return metadata

    def _check_issue_meta(self, metadata):
        """
            This method will check the given metadata and retrieve
            a new dictionary with some new fields.
        """

        issue = Issue(metadata)

        issns = set(
            [
                issue.journal.any_issn(priority=u'electronic'),
                issue.journal.any_issn(priority=u'print'),
                issue.journal.scielo_issn
            ]
        )

        metadata['code'] = issue.publisher_id
        metadata['code_title'] = list(issns)
        metadata['collection'] = issue.collection_acronym
        metadata['issue_type'] = issue.type
        metadata['publication_year'] = issue.publication_date[0:4]
        metadata['publication_date'] = issue.publication_date

        try:
            metadata['processing_date'] = issue.processing_date
        except:
            metadata['processing_date'] = datetime.now().date().isoformat()

        return metadata

    def _check_journal_meta(self, metadata):
        """
            This method will check the given metadata and retrieve
            a new dictionary with some new fields.
        """
        journal = Journal(metadata)

        issns = set([
            journal.any_issn(priority=u'electronic'),
            journal.any_issn(priority=u'print'),
            journal.scielo_issn
        ])

        metadata['code'] = journal.scielo_issn
        metadata['issns'] = list(issns)
        metadata['collection'] = journal.collection_acronym

        try:
            metadata['processing_date'] = journal.processing_date
        except:
            metadata['processing_date'] = datetime.now().date().isoformat()

        return metadata

    def _log_changes(self, document_type, code, event, collection=None, date=None):

        if document_type in ['article', 'journal', 'issue']:
            log_data = {
                'code': code,
                'collection': collection,
                'event': event,
                'date': date or datetime.now().isoformat(),
            }
            log_id = self.db['historychanges_%s' % document_type].insert(log_data)
            return log_id

    def historychanges(self, document_type, collection=None, event=None,
                       code=None, from_date='1500-01-01T00:00:00',
                       until_date=None, limit=LIMIT, offset=0):

        if offset < 0:
            offset = 0

        if limit < 0:
            limit = LIMIT

        fltr = {}
        fltr['date'] = {'$gt': from_date, '$lte': until_date or datetime.now().isoformat()}

        if collection:
            fltr['collection'] = collection

        if event:
            fltr['event'] = event

        if code:
            fltr['code'] = code

        total = self.db['historychanges_%s' % document_type].find(fltr).count()
        data = self.db['historychanges_%s' % document_type].find(fltr).skip(offset).limit(limit).sort("date")

        meta = {
            'limit': limit,
            'offset': offset,
            'filter': fltr,
            'total': total
        }

        objects = [{'date': i['date'], 'code': i['code'], 'collection': i['collection'], 'event': i['event']} for i in data]
        result = {
            'meta': meta,
            'objects': objects
        }
        return result

    def get_journal(self, collection=None, issn=None):

        fltr = {}

        if collection:
            fltr['collection'] = collection

        if issn:
            fltr['code'] = issn

        data = self.db['journals'].find(fltr, {'_id': 0})

        if not data:
            return None

        return [i for i in data]

    @LogHistoryChange(document_type="journal", event_type="delete")
    def delete_journal(self, code, collection=None):

        fltr = {
            'code': code,
            'collection': collection
        }

        deleted = self.db['journals'].delete_one(fltr)

        fltr['deleted_count'] = deleted.deleted_count

        return fltr

    @LogHistoryChange(document_type="journal", event_type="add")
    def add_journal(self, metadata):

        journal = self._check_journal_meta(metadata)

        if not journal:
            return None

        if self.exists_journal(journal['code'], journal['collection']):
            return self.update_journal(journal)

        self.db['journals'].update_one(
            {'code': journal['code'], 'collection': journal['collection']},
            {'$set': journal},
            upsert=True
        )

        return journal

    @LogHistoryChange(document_type="journal", event_type="update")
    def update_journal(self, metadata):

        journal = self._check_issue_meta(metadata)

        if not journal:
            return None

        journal['updated_at'] = datetime.now().date().isoformat()

        self.db['journals'].update_one(
            {'code': journal['code'], 'collection': journal['collection']},
            {'$set': journal},
            upsert=True
        )

        return journal

    def identifiers_collection(self):

        data = self.db['collections'].find({}, {'_id': 0})

        if not data:
            return None

        return [i for i in data]

    def get_collection(self, collection):

        fltr = {'code': collection}

        return self.db['collections'].find_one(fltr, {'_id': 0})

    def collection(self, collection=None):
        """
        DEPRECATED
        """
        warnings.warn("deprecated: replaced by identifiers_collection and get_collection", DeprecationWarning)

        self.get_collection(collection=collection)

    def identifiers_journal(self, collection=None, issn=None, limit=LIMIT, offset=0, extra_filter=None):

        if offset < 0:
            offset = 0

        if limit < 0:
            limit = LIMIT

        fltr = {}
        if collection:
            fltr['collection'] = collection

        if issn:
            fltr['code'] = issn

        if extra_filter:
            fltr.update(json.loads(extra_filter))

        total = self.db['journals'].find(fltr).count()
        data = self.db['journals'].find(fltr, {'code': 1, 'collection': 1, 'processing_date': 1}).skip(offset).limit(limit)

        meta = {'limit': limit,
                'offset': offset,
                'filter': fltr,
                'total': total}

        result = {'meta': meta, 'objects': [{'code': i['code'], 'collection': i['collection'], 'processing_date': i['processing_date']} for i in data]}

        return result

    def identifiers_issue(
            self,
            collection=None,
            issn=None,
            from_date='1500-01-01',
            until_date=None,
            limit=LIMIT,
            offset=0,
            extra_filter=None):

        if offset < 0:
            offset = 0

        if limit < 0:
            limit = LIMIT

        fltr = {}
        fltr['processing_date'] = {'$gte': from_date, '$lte': until_date or datetime.now().date().isoformat()}

        if collection:
            fltr['collection'] = collection

        if issn:
            fltr['code_title'] = issn

        if extra_filter:
            fltr.update(json.loads(extra_filter))

        total = self.db['issues'].find(fltr).count()
        data = self.db['issues'].find(fltr, {
            'code': 1,
            'collection': 1,
            'processing_date': 1}
        ).skip(offset).limit(limit)

        meta = {'limit': limit,
                'offset': offset,
                'filter': fltr,
                'total': total}

        result = {'meta': meta, 'objects': []}
        for i in data:
            rec = {
                'code': i['code'],
                'collection': i['collection'],
                'processing_date': i['processing_date']
            }

            result['objects'].append(rec)

        return result

    def get_issue(self, code, collection=None, replace_journal_metadata=False):

        fltr = {'code': code}

        if collection:
            fltr['collection'] = collection

        data = self.db['issues'].find_one(fltr)

        if not data:
            return None

        if replace_journal_metadata is True:
            journal = self.get_journal(collection=collection, issn=code[0:9])
            if journal and len(journal) != 0:
                data['title'] = journal[0]

        del(data['_id'])

        return data

    def get_issues(self, code, collection=None, replace_journal_metadata=False):

        fltr = {'code': code}

        if collection:
            fltr['collection'] = collection

        data = self.db['issues'].find(fltr, {'_id': 0})

        for issue in data:
            if replace_journal_metadata is True:
                journal = self.get_journal(collection=collection, issn=code[0:9])
                if journal and len(journal) != 0:
                    data['title'] = journal[0]

            yield issue

    def exists_journal(self, code, collection=None):
        fltr = {'code': code}

        if collection:
            fltr['collection'] = collection

        if self.db['journals'].find(fltr).count() >= 1:
            return True

        return False

    def exists_issue(self, code, collection=None):
        fltr = {'code': code}

        if collection:
            fltr['collection'] = collection

        if self.db['issues'].find(fltr).count() >= 1:
            return True

        return False

    @LogHistoryChange(document_type="issue", event_type="delete")
    def delete_issue(self, code, collection=None):

        fltr = {'code': code}

        if collection:
            fltr['collection'] = collection

        deleted = self.db['issues'].delete_one(fltr)

        fltr['deleted_count'] = deleted.deleted_count

        return fltr

    @LogHistoryChange(document_type="issue", event_type="add")
    def add_issue(self, metadata):

        issue = self._check_issue_meta(metadata)

        if not issue:
            return None

        if self.exists_issue(issue['code'], issue['collection']):
            return self.update_issue(metadata)

        issue['created_at'] = issue['processing_date']

        self.db['issues'].update_one(
            {'code': issue['code'], 'collection': issue['collection']},
            {'$set': issue},
            upsert=True
        )

        return issue

    @LogHistoryChange(document_type="issue", event_type="update")
    def update_issue(self, metadata):

        issue = self._check_issue_meta(metadata)

        if not issue:
            return None

        issue['updated_at'] = datetime.now().date().isoformat()

        self.db['issues'].update_one(
            {'code': issue['code'], 'collection': issue['collection']},
            {'$set': issue},
            upsert=True
        )

        return issue

    def identifiers_article(self,
                            collection=None,
                            issn=None,
                            from_date='1500-01-01',
                            until_date=None,
                            limit=LIMIT,
                            offset=0,
                            extra_filter=None):

        if offset < 0:
            offset = 0

        if limit < 0:
            limit = LIMIT

        fltr = {}
        fltr['processing_date'] = {'$gte': from_date, '$lte': until_date or datetime.now().date().isoformat()}

        if collection:
            fltr['collection'] = collection

        if issn:
            fltr['code_title'] = issn

        if extra_filter:
            fltr.update(json.loads(extra_filter))

        total = self.db['articles'].find(fltr).count()
        data = self.db['articles'].find(fltr, {
            'code': 1,
            'collection': 1,
            'processing_date': 1,
            'aid': 1,
            'doi': 1}
        ).skip(offset).limit(limit)

        meta = {'limit': limit,
                'offset': offset,
                'filter': fltr,
                'total': total}

        result = {'meta': meta, 'objects': []}
        for i in data:
            rec = {
                'code': i['code'],
                'collection': i['collection'],
                'processing_date': i['processing_date']
            }
            if 'aid' in i:
                rec['aid'] = i['aid']

            if 'doi' in i:
                rec['doi'] = i['doi']

            result['objects'].append(rec)

        return result

    def identifiers_press_release(self,
                                  collection=None,
                                  issn=None,
                                  from_date='1500-01-01',
                                  until_date=None,
                                  limit=LIMIT,
                                  offset=0):

        if offset < 0:
            offset = 0

        if limit < 0:
            limit = LIMIT

        fltr = {}
        fltr['processing_date'] = {'$gte': from_date, '$lte': until_date or datetime.now().date().isoformat()}

        fltr['document_type'] = u'press-release'

        if collection:
            fltr['collection'] = collection

        if issn:
            fltr['code_title'] = issn

        total = self.db['articles'].find(fltr).count()
        data = self.db['articles'].find(fltr, {
            'code': 1,
            'collection': 1,
            'processing_date': 1,
            'aid': 1,
            'doi': 1}
        ).skip(offset).limit(limit)

        meta = {'limit': limit,
                'offset': offset,
                'filter': fltr,
                'total': total}

        result = {'meta': meta, 'objects': []}
        for i in data:
            rec = {
                'code': i['code'],
                'collection': i['collection'],
                'processing_date': i['processing_date']
            }
            if 'aid' in i:
                rec['aid'] = i['aid']

            if 'doi' in i:
                rec['doi'] = i['doi']

            result['objects'].append(rec)

        return result

    def get_article(self, code, collection=None, replace_journal_metadata=False, body=False):
        """
            replace_journal_metadata: replace the content of the title attribute
            that cames with the article record. The content is replaced by the
            oficial and updated journal record. This may be used in cases that
            the developer intent to retrive the must recent journal data instead
            of the journal data recorded when the article was inserted in the
            collection.
        """

        fltr = {'$or': [{'code': code}, {'doi': code}, {'aid': code}]}
        if collection:
            fltr['collection'] = collection

        fields = None

        if not body:
            fields = {'body': 0}

        if fields:
            data = self.db['articles'].find_one(fltr, fields)
        else:
            data = self.db['articles'].find_one(fltr)

        if not data:
            return None

        if replace_journal_metadata is True:
            journal = self.get_journal(
                collection=collection, issn=data['title']['v400'][0]['_'])

            if journal and len(journal) != 0:
                data['title'] = journal[0]

        issue = self.get_issue(collection=collection, code=data['code'][1:18])

        if issue:
            data['issue'] = issue
            if 'title' in data['issue']:
                del(data['issue']['title'])

        del(data['_id'])

        return data

    def get_articles(self, code, collection=None, replace_journal_metadata=False):

        fltr = {'code': code}
        if collection:
            fltr['collection'] = collection

        data = self.db['articles'].find(fltr, {'_id': 0})

        for article in data:
            if replace_journal_metadata:
                journal = self.get_journal(collection=collection, issn=article['title']['v400'][0]['_'])

                if journal and len(journal) == 1:
                    article['title'] = journal[0]

            issue = self.get_issue(collection=collection, code=article['code_issue'])

            if issue:
                article['issue'] = issue

            yield article

    def exists_article(self, code, collection=None):
        fltr = {'code': code}

        if collection:
            fltr['collection'] = collection

        if self.db['articles'].find(fltr).count() >= 1:
            return True

        return False

    @LogHistoryChange(document_type="article", event_type="delete")
    def delete_article(self, code, collection=None):

        fltr = {'$or': [{'code': code}, {'doi': code}, {'aid': code}]}

        if collection:
            fltr['collection'] = collection

        deleted = self.db['articles'].delete_one(fltr)

        fltr['code'] = code
        fltr['deleted_count'] = deleted.deleted_count

        return fltr


    @LogHistoryChange(document_type="article", event_type="add")
    def add_article(self, metadata):

        article = self._check_article_meta(metadata)

        if not article:
            return None

        if self.exists_article(article['code'], article['collection']):
            return self.update_article(metadata)

        article['created_at'] = article['processing_date']

        self.db['articles'].update_one(
            {'code': article['code'], 'collection': article['collection']},
            {'$set': article},
            upsert=True
        )

        return article

    @LogHistoryChange(document_type="article", event_type="update")
    def update_article(self, metadata):

        article = self._check_article_meta(metadata)

        if not article:
            return None

        article['updated_at'] = datetime.now().date().isoformat()

        self.db['articles'].update_one(
            {'code': article['code'], 'collection': article['collection']},
            {'$set': article},
            upsert=True
        )

        return article

    def set_doaj_id(self, code, collection, doaj_id):

        fltr = {'$or': [{'code': code}, {'doi': code}, {'aid': code}]}

        if collection:
            fltr['collection'] = collection

        self.db['articles'].update_one(fltr, {'$set': {'doaj_id': str(doaj_id)}})

    def set_aid(self, code, collection, aid):

        fltr = {'$or': [{'code': code}, {'doi': code}, {'aid': code}]}

        if collection:
            fltr['collection'] = collection

        self.db['articles'].update_one(fltr, {'$set': {'aid': str(aid)}})
