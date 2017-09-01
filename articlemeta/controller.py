# coding: utf-8
from urllib.parse import urlparse
import warnings
import json

import pymongo
from xylose.scielodocument import Article, Journal, Issue
from articlemeta.decorators import LogHistoryChange
from datetime import datetime

LIMIT = 1000


def dates_to_string(data):

    if 'processing_date' in data and isinstance(data['processing_date'], datetime):
        data['processing_date'] = data['processing_date'].isoformat()[:10]

    if 'processing_date' in data and isinstance(data['processing_date'], dict):
        data['processing_date']['$lte'] = data['processing_date']['$lte'].isoformat()[:10]
        data['processing_date']['$gte'] = data['processing_date']['$gte'].isoformat()[:10]

    if 'date' in data and isinstance(data['date'], datetime):
        data['date'] = data['date'].isoformat()[:10]

    if 'date' in data and isinstance(data['date'], dict):
        data['date']['$lte'] = data['date']['$lte'].isoformat()[:10]
        data['date']['$gte'] = data['date']['$gte'].isoformat()[:10]

    if 'created_at' in data:
        data['created_at'] = data['created_at'].isoformat()[:10]

    if 'updated_at' in data:
        data['updated_at'] = data['updated_at'].isoformat()[:10]

    return data


def get_date_range_filter(from_date=None, until_date=None):

    import datetime

    if until_date is None:
        until_date = datetime.datetime.combine(datetime.datetime.now(), datetime.time.max)
    else:
        until_date = datetime.datetime.strptime(until_date, "%Y-%m-%d")

    filter_range = {
            '$gte': datetime.datetime.strptime(from_date, "%Y-%m-%d"),
            '$lte': until_date
        }

    return filter_range


def get_dbconn(db_dsn):
    """Connects to the MongoDB server and returns a database handler."""

    def _create_indexes(db):
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
                [[('date', pymongo.ASCENDING)], {'background': True}],
                [[('collection', pymongo.ASCENDING)], {'background': True}],
                [[('code', pymongo.ASCENDING)], {'background': True}],
                [[('collection', pymongo.ASCENDING), ('date',  pymongo.ASCENDING)], {'background': True}]
            ],
            'historychanges_journal': [
                [[('date', pymongo.ASCENDING)], {'background': True}],
                [[('collection', pymongo.ASCENDING)], {'background': True}],
                [[('code', pymongo.ASCENDING)], {'background': True}],
                [[('collection', pymongo.ASCENDING), ('date',  pymongo.ASCENDING)], {'background': True}]
            ],
            'historychanges_issue': [
                [[('date', pymongo.ASCENDING)], {'background': True}],
                [[('collection', pymongo.ASCENDING)], {'background': True}],
                [[('code', pymongo.ASCENDING)], {'background': True}],
                [[('collection', pymongo.ASCENDING), ('date',  pymongo.ASCENDING)], {'background': True}]
            ],
            'issues': [
                [[('code', pymongo.ASCENDING)], {'background': True}],
                [[('collection', pymongo.ASCENDING)], {'background': True}],
                [[('processing_date', pymongo.ASCENDING)], {'background': True}],
                [[('publication_year', pymongo.ASCENDING)], {'background': True}],
                [[('code', pymongo.ASCENDING), ('collection',  pymongo.ASCENDING)], {'unique': True, 'background': True}],
                [[('collection', pymongo.ASCENDING), ('processing_date',  pymongo.ASCENDING)], {'background': True}]
            ],
            'journals': [
                [[('code', pymongo.ASCENDING)], {'background': True}],
                [[('code', pymongo.ASCENDING), ('collection',  pymongo.ASCENDING)], {'unique': True, 'background': True}],
                [[('collection', pymongo.ASCENDING), ('processing_date',  pymongo.ASCENDING)], {'background': True}]
            ],
            'articles': [
                [[('document_type', pymongo.ASCENDING)], {'background': True}],
                [[('collection', pymongo.ASCENDING)], {'background': True}],
                [[('code_title', pymongo.ASCENDING)], {'background': True}],
                [[('applicable', pymongo.ASCENDING)], {'background': True}],
                [[('code', pymongo.ASCENDING)], {'background': True}],
                [[('sent_wos', pymongo.ASCENDING)], {'background': True}],
                [[('publication_year', pymongo.ASCENDING)], {'background': True}],
                [[('processing_date', pymongo.ASCENDING)], {'background': True}],
                [[('license', pymongo.ASCENDING)], {'background': True}],
                [[('section', pymongo.ASCENDING)], {'background': True}],
                [[('aid', pymongo.ASCENDING)], {'background': True}],
                [[('version', pymongo.ASCENDING)], {'background': True}],
                [[('code', pymongo.ASCENDING), ('collection',  pymongo.ASCENDING)], {'unique': True, 'background': True}],
                [[('collection', pymongo.ASCENDING), ('processing_date',  pymongo.ASCENDING)], {'background': True}]
            ]
        }

        for collection, indexes in index_by_collection.items():
            for index in indexes:
                print('create index %s (%s)' % (index, collection))
                if len(index) == 1:
                    db[collection].create_index(index[0])
                else:
                    db[collection].create_index(index[0], **index[1])

    print('End Creation index')
    db_url = urlparse(db_dsn)
    conn = pymongo.MongoClient('mongodb://%s' % db_url.netloc)
    db = conn[db_url.path[1:]]
    _create_indexes(db)
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

        if not isinstance(article.processing_date, datetime):
            try:
                metadata['processing_date'] = datetime.strptime(article.processing_date, '%Y-%m-%d')
            except:
                metadata['processing_date'] = datetime.now()

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

        if not isinstance(issue.processing_date, datetime):
            try:
                metadata['processing_date'] = datetime.strptime(issue.processing_date, '%Y-%m-%d')
            except:
                metadata['processing_date'] = datetime.now()

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

        if not isinstance(journal.processing_date, datetime):
            try:
                metadata['processing_date'] = datetime.strptime(journal.processing_date, '%Y-%m-%d')
            except:
                metadata['processing_date'] = datetime.now()

        return metadata

    def _log_changes(self, document_type, code, event, collection=None, date=None):

        if document_type in ['article', 'journal', 'issue']:
            log_data = {
                'code': code,
                'collection': collection,
                'event': event,
                'date': date or datetime.now(),
            }
            log_id = self.db['historychanges_%s' % document_type].insert(log_data)
            return log_id

    def historychanges(self, document_type, collection=None, event=None,
                       code=None, from_date='1997-01-01',
                       until_date=None, limit=LIMIT, offset=0):

        if offset < 0:
            offset = 0

        if limit < 0:
            limit = LIMIT

        fltr = {}

        fltr['date'] = get_date_range_filter(from_date, until_date)

        if collection:
            fltr['collection'] = collection

        if event:
            fltr['event'] = event

        if code:
            fltr['code'] = code

        total = self.db['historychanges_%s' % document_type].find(fltr).count()
        data = self.db['historychanges_%s' % document_type].find(fltr).sort("date").skip(offset).limit(limit)

        meta = {
            'limit': limit,
            'offset': offset,
            'filter': fltr,
            'total': total
        }

        objects = [dates_to_string({'date': i['date'], 'code': i['code'], 'collection': i['collection'], 'event': i['event']}) for i in data]
        result = {
            'meta': meta,
            'objects': objects
        }

        result['meta']['filter'] = dates_to_string(result['meta']['filter'])

        return result

    def get_journal(self, collection=None, issn=None):

        fltr = {}

        if issn:
            fltr['code'] = issn

        if collection:
            fltr['collection'] = collection

        data = self.db['journals'].find(fltr, {'_id': 0})

        if not data:
            return None

        return [dates_to_string(i) for i in data]

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

        journal['created_at'] = journal['processing_date']

        self.db['journals'].update_one(
            {'code': journal['code'], 'collection': journal['collection']},
            {'$set': journal},
            upsert=True
        )

        return dates_to_string(journal)

    @LogHistoryChange(document_type="journal", event_type="update")
    def update_journal(self, metadata):

        journal = self._check_journal_meta(metadata)

        if not journal:
            return None

        journal['updated_at'] = datetime.now()

        self.db['journals'].update_one(
            {'code': journal['code'], 'collection': journal['collection']},
            {'$set': journal},
            upsert=True
        )

        return dates_to_string(journal)

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
        data = self.db['journals'].find(
            fltr,
            {'code': 1, 'collection': 1, 'processing_date': 1}
        ).sort('processing_date').skip(offset).limit(limit)

        meta = {
            'limit': limit,
            'offset': offset,
            'filter': fltr,
            'total': total
        }

        result = {'meta': meta, 'objects': [
            dates_to_string({'code': i['code'], 'collection': i['collection'], 'processing_date': i['processing_date']}) for i in data]}

        result['meta']['filter'] = dates_to_string(result['meta']['filter'])

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
        fltr['processing_date'] = get_date_range_filter(from_date, until_date)

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
        ).sort('processing_date').skip(offset).limit(limit)

        meta = {
            'limit': limit,
            'offset': offset,
            'filter': fltr,
            'total': total
        }

        result = {'meta': meta, 'objects': []}
        for i in data:
            rec = {
                'code': i['code'],
                'collection': i['collection'],
                'processing_date': i['processing_date']
            }

            result['objects'].append(dates_to_string(rec))

        result['meta']['filter'] = dates_to_string(result['meta']['filter'])

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

        return dates_to_string(data)

    def get_issues_full(
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
        fltr['processing_date'] = get_date_range_filter(from_date, until_date)

        if collection:
            fltr['collection'] = collection

        if issn:
            fltr['code_title'] = issn

        if extra_filter:
            fltr.update(json.loads(extra_filter))

        content = {
         '_id': 0
        }

        total = self.db['issues'].find(fltr).count()
        data = self.db['issues'].find(
            fltr, content
        ).sort('processing_date').skip(offset).limit(limit)

        meta = {
            'limit': limit,
            'offset': offset,
            'filter': fltr,
            'total': total
        }

        result = {'meta': meta, 'objects': []}
        for issue in data:
            result['objects'].append(issue)

        result['meta']['filter'] = dates_to_string(result['meta']['filter'])

        return result

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

            yield dates_to_string(issue)

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

        return dates_to_string(issue)

    @LogHistoryChange(document_type="issue", event_type="update")
    def update_issue(self, metadata):

        issue = self._check_issue_meta(metadata)

        if not issue:
            return None

        issue['updated_at'] = datetime.now()

        self.db['issues'].update_one(
            {'code': issue['code'], 'collection': issue['collection']},
            {'$set': issue},
            upsert=True
        )

        return dates_to_string(issue)

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
        fltr['processing_date'] = get_date_range_filter(from_date, until_date)

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
        ).sort('processing_date').skip(offset).limit(limit)

        meta = {
            'limit': limit,
            'offset': offset,
            'filter': fltr,
            'total': total
        }

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

            result['objects'].append(dates_to_string(rec))

        result['meta']['filter'] = dates_to_string(result['meta']['filter'])

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
        fltr['processing_date'] = get_date_range_filter(from_date, until_date)

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
        ).sort('processing_date').skip(offset).limit(limit)

        meta = {
            'limit': limit,
            'offset': offset,
            'filter': fltr,
            'total': total
        }

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

            result['objects'].append(dates_to_string(rec))

        result['meta']['filter'] = dates_to_string(result['meta']['filter'])

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

        return dates_to_string(data)

    def get_articles_full(
        self,
        collection=None,
        issn=None,
        from_date='1500-01-01',
        until_date=None,
        limit=100,
        offset=0,
        extra_filter=None,
        replace_journal_metadata=False,
        body=False
    ):

        if offset < 0:
            offset = 0

        if limit < 0:
            limit = 100

        fltr = {}
        fltr['processing_date'] = get_date_range_filter(from_date, until_date)

        if collection:
            fltr['collection'] = collection

        if issn:
            fltr['code_title'] = issn

        if extra_filter:
            fltr.update(json.loads(extra_filter))

        content = {
            '_id': 0
        }

        if body is False:
            content['body'] = 0

        total = self.db['articles'].find(fltr).count()
        data = self.db['articles'].find(fltr, content
        ).sort('processing_date').skip(offset).limit(limit)

        meta = {
            'limit': limit,
            'offset': offset,
            'filter': fltr,
            'total': total
        }

        result = {'meta': meta, 'objects': []}
        for article in data:
            if replace_journal_metadata:
                journal = self.get_journal(collection=collection, issn=article['title']['v400'][0]['_'])

                if journal and len(journal) == 1:
                    article['title'] = journal[0]

            issue = self.get_issue(collection=collection, code=article['code_issue'])

            if issue:
                article['issue'] = issue

            result['objects'].append(dates_to_string(article))

        result['meta']['filter'] = dates_to_string(result['meta']['filter'])

        return result

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

            yield dates_to_string(article)

    def exists_article(self, code, collection=None):
        fltr = {'code': code}

        if collection:
            fltr['collection'] = collection

        if self.db['articles'].find(fltr).count() >= 1:
            return True

        return False

    @LogHistoryChange(document_type="article", event_type="delete")
    def delete_article(self, code, collection=None):

        fltr = {'code': code}

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

        return dates_to_string(article)

    @LogHistoryChange(document_type="article", event_type="update")
    def update_article(self, metadata):

        article = self._check_article_meta(metadata)

        if not article:
            return None

        article['updated_at'] = datetime.now()

        self.db['articles'].update_one(
            {'code': article['code'], 'collection': article['collection']},
            {'$set': article},
            upsert=True
        )

        return dates_to_string(article)

    def set_doaj_id(self, code, collection, doaj_id):

        fltr = {'code': code}

        if collection:
            fltr['collection'] = collection

        self.db['articles'].update_one(fltr, {'$set': {'doaj_id': str(doaj_id)}})

    def set_aid(self, code, collection, aid):

        fltr = {'code': code}

        if collection:
            fltr['collection'] = collection

        self.db['articles'].update_one(fltr, {'$set': {'aid': str(aid)}})
