# coding: utf-8
import unicodedata
from datetime import datetime, timedelta
import urlparse

import pymongo
from xylose.scielodocument import Article, Journal
from decorators import LogHistoryChange


def remove_accents(data):

    if not isinstance(data, unicode):
        unicode(data)

    try:
        return u''.join(x for x in unicodedata.normalize('NFKD', data) if unicodedata.category(x)[0] == 'L').lower()
    except:
        return u''


def gen_citations_title_keys(article):
    """
    This method is responsible to receive an array having the article titles
    available for the a given article and convert then into keys exemple.
    from: ['Health care after 60th', 'Cuidados de saúde após os sessenta anos']
    to: ['healthcareafter60th', 'cuidadosdesaudeaposossessentaanos']
    """

    def get_citation_titles():
        titles = set()

        for citation in article.citations:
            title = ''
            if citation.article_title:
                title = citation.article_title
            elif citation.chapter_title:
                title = citation.chapter_title
            elif citation.thesis_title:
                title = citation.thesis_title
            elif citation.conference_title:
                title = citation.conference_title
            elif citation.link_title:
                title = citation.link_title

            if not title:
                continue

            noaccents_title = remove_accents(title)
            if not noaccents_title:
                continue

            titles.add(noaccents_title)

        if len(titles) == 0:
            return []

        return list(titles)

    def get_citation_titles_pages():
        titles = set()

        for citation in article.citations:
            title = ''
            if citation.article_title:
                title = citation.article_title
            elif citation.chapter_title:
                title = citation.chapter_title
            elif citation.thesis_title:
                title = citation.thesis_title
            elif citation.conference_title:
                title = citation.conference_title
            elif citation.link_title:
                title = citation.link_title

            if not title:
                continue

            start_page = citation.start_page or ''
            end_page = citation.end_page or ''

            noaccents_title = remove_accents(title)
            if not noaccents_title:
                continue

            titles.add(noaccents_title+start_page+end_page)


        if len(titles) == 0:
            return []

        return list(titles)

    def get_citation_titles_author_year():
        titles = set()

        for citation in article.citations:

            if not citation.date:
                continue

            data = []
            title = ''
            if citation.article_title:
                title = citation.article_title
            elif citation.chapter_title:
                title = citation.chapter_title
            elif citation.thesis_title:
                title = citation.thesis_title
            elif citation.conference_title:
                title = citation.conference_title
            elif citation.link_title:
                title = citation.link_title

            if not title:
                continue

            data.append(title)

            author = ''
            if citation.authors:
                author = citation.authors[0].get('given_names', '')+citation.authors[0].get('surname', '')
            elif citation.monographic_authors:
                author = citation.monographic_authors[0].get('given_names', '')+citation.monographic_authors[0].get('surname', '')

            if not author:
                continue

            data.append(author)

            noaccents_title_author = remove_accents(''.join(data))
            if not noaccents_title_author:
                continue

            key = remove_accents(noaccents_title_author)

            key += citation.date[0:4]

            if key:
                titles.add(key)

        if len(titles) == 0:
            return []

        return list(titles)

    if not article.citations:
        return []

    no_accents_strings = get_citation_titles()
    no_accents_strings_author_year = get_citation_titles_author_year()
    no_accents_strings_pages = get_citation_titles_pages()

    if not no_accents_strings:
        return []

    title_keys = {}
    title_keys['citations_keys'] = no_accents_strings + no_accents_strings_author_year + no_accents_strings_pages

    return title_keys


def gen_title_keys(article):
    """
    This method is responsible to receive an array having the article titles
    available for the a given article and convert then into keys exemple.
    from: ['Health care after 60th', 'Cuidados de saúde após os sessenta anos']
    to: ['healthcareafter60th', 'cuidadosdesaudeaposossessentaanos']
    """

    def titles():
        titles = []
        if article.original_title():
            titles.append(article.original_title())

        if article.translated_titles():
            for title in article.translated_titles().values():
                titles.append(title)

        if len(titles) == 0:
            return []

        return titles

    titles = titles()

    if not titles:
        return []

    no_accents_strings = []
    no_accents_strings_author_year = []
    for title in titles:
        noaccents_title = remove_accents(title)
        if not noaccents_title:
            continue
        ra = noaccents_title
        no_accents_strings.append(ra)

        if not article.authors:
            continue

        author = article.authors[0].get('given_names', '')+article.authors[0].get('surname', '')
        author = remove_accents(author)
        no_accents_strings_author_year.append(
            ra+author+article.publication_date[0:4])

    title_keys = {}
    title_keys['title_keys'] = no_accents_strings + no_accents_strings_author_year

    return title_keys


def get_dbconn(db_dsn):
    """Connects to the MongoDB server and returns a database handler.
    """
    db_url = urlparse.urlparse(db_dsn)
    conn = pymongo.Connection(host=db_url.hostname, port=db_url.port)
    db = conn[db_url.path[1:]]
    if db_url.username and db_url.password:
        db.authenticate(db_url.username, db_url.password)

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

        issns = set([article.journal.any_issn(priority=u'electronic'),
                    article.journal.any_issn(priority=u'print')])

        metadata['code_issue'] = article.publisher_id[1:18]
        metadata['code_title'] = list(issns)
        metadata['collection'] = article.collection_acronym
        metadata['document_type'] = article.document_type
        metadata['publication_year'] = article.publication_date[0:4]
        metadata['validated_scielo'] = 'False'
        metadata['validated_wos'] = 'False'
        metadata['sent_wos'] = 'False'
        metadata['sent_doaj'] = 'False'
        metadata['applicable'] = 'False'

        if article.doi:
            metadata['doi'] = article.doi

        try:
            metadata['processing_date'] = article.processing_date
        except:
            if article.publication_date > datetime.now().date().isoformat():
                metadata['processing_date'] = datetime.now().date().isoformat()

        gtk = gen_title_keys(article)
        if gtk:
            metadata.update(gtk)

        gctk = gen_citations_title_keys(article)
        if gctk:
            metadata.update(gctk)

        return metadata

    def _check_journal_meta(self, metadata):
        """
            This method will check the given metadata and retrieve
            a new dictionary with some new fields.
        """
        journal = Journal(metadata)

        issns = set([journal.any_issn(priority=u'electronic'),
                     journal.any_issn(priority=u'print')])

        metadata['code'] = list(issns)
        metadata['collection'] = journal.collection_acronym

        return metadata

    def _log_changes(self, document_type, pid, event, collection=None, date=None):

        if document_type in ['article', 'journal']:
            log_data = {
                'pid': pid,
                'collection': collection,
                'event': event,
                'date': date or datetime.now().isoformat(),
            }
            log_id = self.db['historychanges_%s' % document_type].insert(log_data)
            return log_id

    def historychanges(self, document_type, collection=None, event=None,
                       pid=None, from_date='1500-01-01T00:00:00',
                       until_date=None, limit=1000, offset=0):
        fltr = {}
        fltr['date'] = {'$gt': from_date, '$lte': until_date or datetime.now().isoformat()}

        if collection:
            fltr['collection'] = collection

        if event:
            fltr['event'] = event

        if pid:
            fltr['pid'] = pid

        total = self.db['historychanges_%s' % document_type].find(fltr).count()
        data = self.db['historychanges_%s' % document_type].find(fltr).skip(offset).limit(limit).sort("date")

        meta = {
            'limit': limit,
            'offset': offset,
            'filter': fltr,
            'total': total
        }

        objects = [{'date': i['date'], 'pid': i['pid'], 'collection': i['collection'], 'event': i['event']} for i in data]
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
    def delete_journal(self, issn, collection=None):

        fltr = {
            'code': issn,
            'collection': collection
        }

        self.db['journals'].remove(fltr)

        return fltr

    @LogHistoryChange(document_type="journal", event_type="add")
    def add_journal(self, metadata):

        journal = self._check_journal_meta(metadata)

        if not journal:
            return None

        self.db['journals'].update(
            {'code': journal['code'], 'collection': journal['collection']},
            {'$set': journal},
            safe=False,
            upsert=True
        )

        return journal

    def collection(self):

        data = self.db['collections'].find({}, {'_id': 0})

        if not data:
            return None

        return [i for i in data]

    def identifiers_journal(self, collection=None, limit=1000, offset=0):

        fltr = {}
        if collection:
            fltr['collection'] = collection

        total = self.db['journals'].find(fltr).count()
        data = self.db['journals'].find(fltr, {'code': 1, 'collection': 1}).skip(offset).limit(limit)

        meta = {'limit': limit,
                'offset': offset,
                'filter': fltr,
                'total': total}

        result = {'meta': meta, 'objects': [{'code': i['code'], 'collection': i['collection']} for i in data]}

        return result

    def identifiers_article(self,
                            collection=None,
                            from_date='1500-01-01',
                            until_date=None,
                            limit=1000,
                            offset=0):

        fltr = {}
        fltr['processing_date'] = {'$gte': from_date, '$lte': until_date or datetime.now().date().isoformat()}

        hint = [('processing_date', -1)]
        if collection:
            fltr['collection'] = collection
            hint.insert(0, ('collection', 1))

        total = self.db['articles'].find(fltr).hint(hint).count()
        data = self.db['articles'].find(fltr, {
            'code': 1,
            'collection': 1,
            'processing_date': 1}
        ).hint(hint).skip(offset).limit(limit)

        meta = {'limit': limit,
                'offset': offset,
                'filter': fltr,
                'total': total}

        result = {'meta': meta, 'objects': [{'code': i['code'], 'collection': i['collection'], 'processing_date': i['processing_date']} for i in data]}

        return result

    def identifiers_press_release(self,
                                  collection=None,
                                  from_date='1500-01-01',
                                  until_date=None,
                                  limit=1000,
                                  offset=0):

        fltr = {}
        fltr['processing_date'] = {'$gte': from_date, '$lte': until_date or datetime.now().date().isoformat()}

        fltr['document_type'] = u'press-release'

        if collection:
            fltr['collection'] = collection

        total = self.db['articles'].find(fltr).hint([('document_type', 1), ('collection', 1), ('processing_date', -1)]).count()
        data = self.db['articles'].find(fltr, {
            'code': 1,
            'collection': 1,
            'processing_date': 1}
        ).hint([('document_type', 1), ('collection', 1), ('processing_date', -1)]).skip(offset).limit(limit)

        meta = {'limit': limit,
                'offset': offset,
                'filter': fltr,
                'total': total}

        result = {'meta': meta, 'objects': [{'code': i['code'], 'collection': i['collection'], 'processing_date': i['processing_date']} for i in data]}

        return result

    def get_article(self, code, collection=None, replace_journal_metadata=False):
        """
            replace_journal_metadata: replace the content of the title attribute
            that cames with the article record. The content is replaced by the
            oficial and updated journal record. This may be used in cases that
            the developer intent to retrive the must recent journal data instead
            of the journal data recorded when the article was inserted in the
            collection.
        """

        fltr = {'code': code}
        if collection:
            fltr['collection'] = collection

        data = self.db['articles'].find_one(fltr)

        if not data:
            return None

        if replace_journal_metadata:
            journal = self.get_journal(collection=collection, issn=data['title']['v400'][0]['_'])

            if journal and len(journal) != 0:
                data['title'] = journal[0]

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

        fltr = {
            'code': code,
            'collection': collection
        }

        self.db['articles'].remove(fltr)

        return fltr

    @LogHistoryChange(document_type="article", event_type="add")
    def add_article(self, metadata):

        article = self._check_article_meta(metadata)

        if not article:
            return None

        code = article['article']['v880'][0]['_']
        collection = article['article']['v992'][0]['_']

        article['created_at'] = article['processing_date']

        self.db['articles'].update(
            {'code': code, 'collection': collection},
            {'$set': article},
            safe=False,
            upsert=True
        )

        return article

    @LogHistoryChange(document_type="article", event_type="update")
    def update_article(self, metadata):

        article = self._check_article_meta(metadata)

        if not article:
            return None

        code = article['article']['v880'][0]['_']
        collection = article['article']['v992'][0]['_']

        self.db['articles'].update(
            {'code': code, 'collection': collection},
            {'$set': article},
            safe=False,
            upsert=True
        )

        return article

    def set_doaj_status(self, code, status):

        self.db['articles'].update(
            {'code': code},
            {'$set': {'sent_doaj': str(status)}},
            safe=False
        )
