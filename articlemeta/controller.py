# coding: utf-8
from urllib.parse import urlparse
import warnings
import json

import pymongo
from xylose.scielodocument import Article, Journal, Issue
from articlemeta.decorators import LogHistoryChange
from articlemeta.data import COLLECTIONS_PATH
from datetime import datetime
import requests

LIMIT = 1000


def dates_to_string(data):
    """Convert instances of datetime to text in YYYY-MM-DD format,
    up to ``sys.getrecursionlimit()`` levels of depth.

    :param data: data dictionary
    """
    datacopy = data.copy()
    newdata = {}

    for key, value in datacopy.items():
        if hasattr(value, 'isoformat'):
            newdata[key] = value.isoformat()[:10]
        elif hasattr(value, 'items'):
            newdata[key] = dates_to_string(value)
        else:
            newdata[key] = value

    datacopy.update(newdata)
    return datacopy


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
                [[('code_title', pymongo.ASCENDING)], {'background': True}],
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
            ],
            'name_suffixes': [
                [[('suffix', pymongo.ASCENDING)], {'background': True}],
            ],
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


class IssueMeta:
    def __init__(self, db, journalmeta):
        self.db = db
        self.journalmeta = journalmeta

    def check(self, metadata):
        """Enriquece e normaliza itens do dicionário ``metadata``, que representa
        metadados de um fascículo.

        A estrutura de ``metadata`` é a mesma retornada pelo formato JSON, do
        ``articlemeta.scielo.org``, conforme exemplo:
        https://gist.github.com/gustavofonseca/4a5919db8d0027f37522da7d06bfa876
        """
        metadata_copy = metadata.copy()
        issue = Issue(metadata_copy)

        issns = set(
            [
                issue.journal.any_issn(priority=u'electronic'),
                issue.journal.any_issn(priority=u'print'),
                issue.journal.scielo_issn
            ]
        )

        metadata_copy['code'] = issue.publisher_id
        metadata_copy['code_title'] = list(issns)
        metadata_copy['collection'] = issue.collection_acronym
        metadata_copy['issue_type'] = issue.type
        metadata_copy['publication_year'] = issue.publication_date[0:4]
        metadata_copy['publication_date'] = issue.publication_date

        if not isinstance(issue.data['issue']['processing_date'], datetime):
            try:
                metadata_copy['processing_date'] = datetime.strptime(issue.data['issue']['processing_date'], '%Y-%m-%d')
            except:
                metadata_copy['processing_date'] = datetime.now()

        return metadata_copy

    def identifiers(self, collection=None, issn=None,
            from_date='1500-01-01', until_date=None, limit=None, offset=0,
            extra_filter=None):
        """Lista os códigos identificadores dos fascículos. A listagem pode ser
        completa, por coleção, por ISSN ou por intervalo da data de processamento.
        """
        if offset < 0:
            offset = 0

        if limit is None or limit < 0:
            limit = LIMIT

        fltr = {}
        fltr['processing_date'] = get_date_range_filter(from_date, until_date)

        if collection:
            fltr['collection'] = collection

        if issn:
            fltr['code_title'] = issn

        if extra_filter:
            fltr.update(json.loads(extra_filter))

        total = self.db.find(fltr).count()
        data = self.db.find(fltr, {
            'code': 1, 'collection': 1, 'processing_date': 1}).sort(
                    'processing_date').skip(offset).limit(limit)

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

    def get(self, code, collection=None, replace_journal_metadata=False):
        """Obtém um fascículo de código identificador ``code``. Opcionalmente,
        um acrônimo de coleção pode ser passado por meio do arg ``collection``
        para especializar a busca.

        O arg ``replace_journal_metadata`` faz com que o resultado da
        consulta contenha a versão mais atualizada dos metadados do periódico.

        Retorna um dicionário ou None.
        """
        fltr = {'code': code}
        if collection:
            fltr['collection'] = collection

        data = self.db.find_one(fltr)

        if not data:
            return None

        if replace_journal_metadata:
            journal = self.journalmeta.get(collection=collection, issn=code[0:9])
            if journal and len(journal) != 0:
                data['title'] = journal[0]

        del(data['_id'])

        return dates_to_string(data)

    def get_issues_full(self, collection=None, issn=None, from_date='1500-01-01',
            until_date=None, limit=LIMIT, offset=0, extra_filter=None):
        """Obtém uma lista dos fascículos, que pode ser geral, por coleção,
        por periódico ou intervalo de data de publicação. Há ainda a
        possibilidade de usar filtros adhoc por meio de consultas diretas ao
        MongoDB com o arg ``extra_filter`` (alto acoplamento; não recomendado).
        """
        if offset < 0:
            offset = 0

        if limit is None or limit < 0:
            limit = LIMIT

        fltr = {}
        fltr['processing_date'] = get_date_range_filter(from_date, until_date)

        if collection:
            fltr['collection'] = collection

        if issn:
            fltr['code_title'] = issn

        if extra_filter:
            fltr.update(json.loads(extra_filter))

        total = self.db.find(fltr).count()
        data = self.db.find(fltr, {'_id': 0}).sort(
                'processing_date').skip(offset).limit(limit)

        meta = {
                'limit': limit,
                'offset': offset,
                'filter': fltr,
                'total': total,
                }

        result = {'meta': meta, 'objects': []}
        for issue in data:
            result['objects'].append(dates_to_string(issue))

        result['meta']['filter'] = dates_to_string(result['meta']['filter'])

        return result

    def exists(self, code, collection=None):
        """Se o fascículo de código ``code`` existe. A consulta pode ser
        realizada no contexto global ou de coleção.
        """
        fltr = {'code': code}
        if collection:
            fltr['collection'] = collection

        if self.db.find(fltr).count() >= 1:
            return True

        return False

    def delete(self, code, collection=None):
        """Remove o fascículo de código igual a ``code``, da coleção
        ``collection``.

        Retorna um dicionário na forma:

        .. code-block:: python

            {'code': '0104-326920150002', 'collection': 'scl', 'deleted_count': 1}
        """
        fltr = {'code': code}
        if collection:
            fltr['collection'] = collection

        deleted = self.db.delete_one(fltr)

        fltr['deleted_count'] = deleted.deleted_count

        return fltr

    def add(self, metadata):
        """Registra o fascículo representado por ``metadata``.

        Retorna uma cópia enriquecida do dicionário ``metadata``, com o
        acréscimo da chave ``created_at``.
        """
        issue = self.check(metadata)

        if not issue:
            return None

        if self.exists(issue['code'], issue['collection']):
            return self.update(issue)

        issue['created_at'] = issue['processing_date']

        self.db.update_one(
                {'code': issue['code'], 'collection': issue['collection']},
                {'$set': issue},
                upsert=True)

        return dates_to_string(issue)

    def update(self, metadata):
        """Atualiza o registro do fascículo representado por ``metadata``.

        Retorna uma cópia enriquecida do dicionário ``metadata``, com o
        acréscimo da chave ``updated_at``.
        """
        issue = self.check(metadata)

        if not issue:
            return None

        issue['updated_at'] = datetime.now()

        self.db.update_one(
                {'code': issue['code'], 'collection': issue['collection']},
                {'$set': issue},
                upsert=True)

        return dates_to_string(issue)

    def get_code_from_label(self, label, journal_code, collection):
        """Retorna o `code` de um fasciculo a partir do seu `label`.

        Tenta encontrar o label em 2 estruturas de dados distintas: primeiro
        em uma string e segundo em uma lista de dicts.
        """
        return self._get_code_from_label_str(label, journal_code,
                collection) or self._get_code_from_label_list(label,
                        journal_code, collection)

    def _get_code_from_label_list(self, label, journal_code, collection):
        fltr = {
                'collection': collection,
                'code_title': journal_code,
                'issue.v4': {'$elemMatch': {'_': label}},
                }
        projection = {'code': True, '_id': False}

        data = self.db.find_one(fltr, projection)
        try:
            return data.get('code', '')
        except AttributeError:
            return ''

    def _get_code_from_label_str(self, label, journal_code, collection):
        fltr = {
                'collection': collection,
                'code_title': journal_code,
                'issue.v4': label,
                }
        projection = {'code': True, '_id': False}

        data = self.db.find_one(fltr, projection)
        try:
            return data.get('code', '')
        except AttributeError:
            return ''


class JournalMeta:
    def __init__(self, db):
        self.db = db

    def check(self, metadata):
        """Enriquece e normaliza itens do dicionário ``metadata``, que representa
        metadados de um periódico.

        A estrutura de ``metadata`` é a mesma retornada pelo formato JSON, do
        ``articlemeta.scielo.org``, conforme exemplo:
        https://gist.github.com/gustavofonseca/92638fe6e1f85dd84bcebce72e83b76e
        """
        metadata_copy = metadata.copy()
        journal = Journal(metadata_copy)

        issns = set([
            journal.any_issn(priority=u'electronic'),
            journal.any_issn(priority=u'print'),
            journal.scielo_issn
        ])

        metadata_copy['code'] = journal.scielo_issn
        metadata_copy['issns'] = list(issns)
        metadata_copy['collection'] = journal.collection_acronym

        if not isinstance(journal.data['processing_date'], datetime):
            try:
                metadata_copy['processing_date'] = datetime.strptime(journal.data['processing_date'], '%Y-%m-%d')
            except:
                metadata_copy['processing_date'] = datetime.now()

        return metadata_copy

    def get(self, collection=None, issn=None):
        """Obtém uma lista de periódicos que pode ser filtrada por coleção e/ou
        por ISSN.

        Retorna uma lista de dicionários ou None.
        """
        fltr = {}
        if issn:
            fltr['code'] = issn

        if collection:
            fltr['collection'] = collection

        data = self.db.find(fltr, {'_id': 0})

        if not data:
            return None

        return [dates_to_string(i) for i in data]

    def delete(self, code, collection):
        """Remove o periódico de ISSN igual a ``code``, da coleção
        ``collection``.

        Retorna um dicionário na forma:

        .. code-block:: python

            {'code': '0104-3269', 'collection': 'scl', 'deleted_count': 1}
        """
        fltr = {
                'code': code,
                'collection': collection,
                }
        deleted = self.db.delete_one(fltr)
        fltr['deleted_count'] = deleted.deleted_count
        return fltr

    def add(self, metadata):
        """Registra o periódico representado por ``metadata``.

        Retorna uma cópia enriquecida do dicionário ``metadata``, com o
        acréscimo da chave ``created_at``.
        """
        journal = self.check(metadata)

        if not journal:
            return None

        # aqui tem um comportamento de upsert!
        if self.exists(journal['code'], journal['collection']):
            return self.update(journal)

        journal['created_at'] = journal['processing_date']

        self.db.update_one(
                {'code': journal['code'], 'collection': journal['collection']},
                {'$set': journal},
                upsert=True
        )

        return dates_to_string(journal)

    def update(self, metadata):
        """Atualiza o registro do periódico representado por ``metadata``.

        Retorna uma cópia enriquecida do dicionário ``metadata``, com o
        acréscimo da chave ``updated_at``.
        """
        journal = self.check(metadata)

        if not journal:
            return None

        journal['updated_at'] = datetime.now()

        self.db.update_one(
            {'code': journal['code'], 'collection': journal['collection']},
            {'$set': journal},
            upsert=True
        )

        return dates_to_string(journal)

    def identifiers(self, collection=None, issn=None, limit=None,
            offset=0, extra_filter=None):
        """Lista os códigos identificadores dos periódicos. A listagem pode ser
        completa, por coleção ou por ISSN (Fabio e eu pensamos que a listagem
        por ISSN não faz sentido, e o arg ``issn`` deveria ser removido).
        """
        if offset < 0:
            offset = 0

        if limit is None or limit < 0:
            limit = LIMIT

        fltr = {}
        if collection:
            fltr['collection'] = collection

        if issn:
            fltr['code'] = issn

        if extra_filter:
            fltr.update(json.loads(extra_filter))

        total = self.db.find(fltr).count()
        data = self.db.find(
                fltr,
                {'code': 1, 'collection': 1, 'processing_date': 1}).sort(
                        'processing_date').skip(offset).limit(limit)

        meta = {
                'limit': limit,
                'offset': offset,
                'filter': fltr,
                'total': total,
                }

        result = {
                'meta': meta,
                'objects': [
                    dates_to_string({
                        'code': d['code'],
                        'collection': d['collection'],
                        'processing_date': d['processing_date']}) for d in data]}

        result['meta']['filter'] = dates_to_string(result['meta']['filter'])

        return result

    def exists(self, code, collection=None):
        """Se o periódico de código ``code`` existe. A consulta pode ser
        realizada no contexto global ou de coleção.
        """
        fltr = {'code': code}

        if collection:
            fltr['collection'] = collection

        if self.db.find(fltr).count() >= 1:
            return True

        return False


class ArticleMeta:
    def __init__(self, db, journalmeta, issuemeta):
        self.db = db
        self.journalmeta = journalmeta
        self.issuemeta = issuemeta

    def check(self, metadata):
        """Enriquece e normaliza itens do dicionário ``metadata``, que representa
        metadados de um artigo.

        A estrutura de ``metadata`` é a mesma retornada pelo formato JSON, do
        ``articlemeta.scielo.org``, conforme exemplo:
        https://gist.github.com/gustavofonseca/2b970721e587fe639b7ccffd5ea9fc96
        """
        metadata_copy = metadata.copy()
        article = Article(metadata_copy)

        issns = set(
            [
                article.journal.any_issn(priority=u'electronic'),
                article.journal.any_issn(priority=u'print'),
                article.journal.scielo_issn
            ]
        )

        metadata_copy['code'] = article.publisher_id
        metadata_copy['code_issue'] = article.publisher_id[1:18]
        metadata_copy['code_title'] = list(issns)
        metadata_copy['collection'] = article.collection_acronym
        metadata_copy['document_type'] = article.document_type
        metadata_copy['publication_year'] = article.publication_date[0:4]
        metadata_copy['publication_date'] = article.publication_date
        metadata_copy['validated_scielo'] = 'False'
        metadata_copy['validated_wos'] = 'False'
        metadata_copy['sent_wos'] = 'False'
        metadata_copy['applicable'] = 'False'
        metadata_copy['version'] = article.data_model_version

        if article.doi:
            metadata_copy['doi'] = article.doi.upper()

        if not isinstance(article.data['article']['processing_date'], datetime):
            try:
                metadata_copy['processing_date'] = datetime.strptime(article.data['article']['processing_date'], '%Y-%m-%d')
            except:
                metadata_copy['processing_date'] = datetime.now()

        return metadata_copy

    def identifiers(self, collection=None, issn=None, from_date='1500-01-01',
            until_date=None, limit=LIMIT, offset=0, extra_filter=None):
        """Lista os códigos identificadores dos artigos. A listagem pode ser
        completa, por coleção, por ISSN ou por intervalo da data de processamento.
        """
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

        total = self.db.find(fltr).count()
        data = self.db.find(fltr, {
            'code': 1,
            'collection': 1,
            'processing_date': 1,
            'aid': 1,
            'doi': 1}).sort('processing_date').skip(offset).limit(limit)

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

    def get(self, code, collection=None, replace_journal_metadata=False, body=False):
        """Obtém um artigo de código identificador ``code``. Opcionalmente,
        um acrônimo de coleção pode ser passado por meio do arg ``collection``
        para especializar a busca. O código identificador poderá ser: o código
        de fato, o doi ou o aid do artigo.

        O arg ``replace_journal_metadata`` faz com que o resultado da
        consulta contenha a versão mais atualizada dos metadados do periódico.
        Os metadados do fascículo são sempre atualizados.

        Retorna um dicionário ou None.
        """
        fltr = {'$or': [{'code': code}, {'doi': code}, {'aid': code}]}
        if collection:
            fltr['collection'] = collection

        fields = None

        if not body:
            fields = {'body': 0}

        if fields:
            data = self.db.find_one(fltr, fields)
        else:
            data = self.db.find_one(fltr)

        if not data:
            return None

        if replace_journal_metadata is True:
            journal = self.journalmeta.get(collection=collection,
                    issn=data['title']['v400'][0]['_'])

            if journal and len(journal) != 0:
                data['title'] = journal[0]

        issue = self.issuemeta.get(collection=collection, code=data['code'][1:18])

        if issue:
            data['issue'] = issue
            if 'title' in data['issue']:
                del(data['issue']['title'])

        del(data['_id'])

        return dates_to_string(data)

    def get_articles_full(self, collection=None, issn=None,
            from_date='1500-01-01', until_date=None, limit=100, offset=0,
            extra_filter=None, replace_journal_metadata=False, body=False):
        """Obtém uma lista dos artigos, que pode ser geral, por coleção,
        por periódico ou intervalo de data de publicação. Há ainda a
        possibilidade de usar filtros adhoc por meio de consultas diretas ao
        MongoDB com o arg ``extra_filter`` (alto acoplamento; não recomendado).

        O arg ``replace_journal_metadata`` faz com que o resultado da
        consulta contenha a versão mais atualizada dos metadados do periódico.
        Os metadados do fascículo são sempre atualizados.
        """
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

        total = self.db.find(fltr).count()
        data = self.db.find(fltr, content).sort(
                'processing_date').skip(offset).limit(limit)

        meta = {
            'limit': limit,
            'offset': offset,
            'filter': fltr,
            'total': total
        }

        result = {'meta': meta, 'objects': []}
        for article in data:
            if replace_journal_metadata:
                journal = self.journalmeta.get(collection=collection,
                        issn=article['title']['v400'][0]['_'])

                if journal and len(journal) == 1:
                    article['title'] = journal[0]

            issue = self.issuemeta.get(collection=collection,
                    code=article['code_issue'])

            if issue:
                article['issue'] = issue

            result['objects'].append(dates_to_string(article))

        result['meta']['filter'] = dates_to_string(result['meta']['filter'])

        return result

    def exists(self, code, collection=None):
        """Se o artigo de código ``code`` existe. A consulta pode ser
        realizada no contexto global ou de coleção.
        """
        fltr = {'code': code}
        if collection:
            fltr['collection'] = collection

        if self.db.find(fltr).count() >= 1:
            return True

        return False

    def delete(self, code, collection=None):
        """Remove o artigo de código igual a ``code``, da coleção
        ``collection``.

        Retorna um dicionário na forma:

        .. code-block:: python

            {'code': '0104-32692015000200008', 'collection': 'scl', 'deleted_count': 1}
        """
        fltr = {'code': code}
        if collection:
            fltr['collection'] = collection

        deleted = self.db.delete_one(fltr)

        fltr['code'] = code
        fltr['deleted_count'] = deleted.deleted_count

        return fltr

    def add(self, metadata):
        """Registra o artigo representado por ``metadata``.

        Retorna uma cópia enriquecida do dicionário ``metadata``, com o
        acréscimo da chave ``created_at``.
        """
        article = self.check(metadata)

        if not article:
            return None

        if self.exists(article['code'], article['collection']):
            return self.update(article)

        article['created_at'] = article['processing_date']

        self.db.update_one(
            {'code': article['code'], 'collection': article['collection']},
            {'$set': article},
            upsert=True
        )

        return dates_to_string(article)

    def update(self, metadata):
        """Atualiza o registro do artigo representado por ``metadata``.

        Retorna uma cópia enriquecida do dicionário ``metadata``, com o
        acréscimo da chave ``updated_at``.
        """
        article = self.check(metadata)

        if not article:
            return None

        article['updated_at'] = datetime.now()

        self.db.update_one(
            {'code': article['code'], 'collection': article['collection']},
            {'$set': article},
            upsert=True
        )

        return dates_to_string(article)

    def identifiers_press_release(self, collection=None, issn=None,
            from_date='1500-01-01', until_date=None, limit=LIMIT, offset=0):
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

        total = self.db.find(fltr).count()
        data = self.db.find(fltr, {
            'code': 1,
            'collection': 1,
            'processing_date': 1,
            'aid': 1,
            'doi': 1}).sort('processing_date').skip(offset).limit(limit)

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

    def set_doaj_id(self, code, collection, doaj_id):
        fltr = {'code': code}
        if collection:
            fltr['collection'] = collection

        self.db.update_one(fltr, {'$set': {'doaj_id': str(doaj_id)}})

    def set_aid(self, code, collection, aid):
        fltr = {'code': code}
        if collection:
            fltr['collection'] = collection

        self.db.update_one(fltr, {'$set': {'aid': str(aid)}})


class CollectionMeta:
    def __init__(self, pubstatus, filepath=COLLECTIONS_PATH):
        self._filepath = filepath
        self._pubstatus = pubstatus

    @property
    def _data(self):
        with open(self._filepath) as f:
            return json.load(f)

    def _add_counts(self, data, docs_count):
        data['document_count'] = docs_count.get(data.get('acron'))
        data['journal_count'] = self._pubstatus.journals_count(data.get('acron'))

    def identifiers(self):
        docs_count = self._pubstatus.documents_count()
        collections = self._data
        [self._add_counts(collection, docs_count) 
         for collection in collections if collection.get('type') == 'journals']
        return collections

    def get(self, collection):
        for identifier in self._data:
            if identifier.get('acron') == collection:
                if identifier.get('type') == 'journals':
                    docs_count = self._pubstatus.documents_count()
                    self._add_counts(identifier, docs_count)
                return identifier
        else:
            return None


class PublicationStatus:
    def __init__(self, host='http://publication.scielo.org'):
        self._host = host

    def documents_count(self):
        try:
            data = requests.get(self._host+'/api/v1/documents?aggs=collection', timeout=1).json()
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            data = {}
        return {item['key']: item['doc_count'] for item in data.get('collection', {}).get('buckets', [])}

    def journals_count(self, collection):
        try:
            data = requests.get(self._host+'/api/v1/journals?aggs=status&collection=%s' % collection, timeout=0.5).json()
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            data = {}
        return {item['key']: item['doc_count'] for item in data.get('status', {}).get('buckets', [])}


class DataBroker(object):
    def __init__(self, db_client):
        self.db = db_client
        self.journalmeta = JournalMeta(self.db['journals'])
        self.issuemeta = IssueMeta(self.db['issues'], self.journalmeta)
        self.articlemeta = ArticleMeta(self.db['articles'], self.journalmeta,
                                       self.issuemeta)
        pubstatus = PublicationStatus()
        self.collectionmeta = CollectionMeta(pubstatus=pubstatus)

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
        return self.journalmeta.get(collection=collection, issn=issn)

    @LogHistoryChange(document_type="journal", event_type="delete")
    def delete_journal(self, code, collection=None):
        return self.journalmeta.delete(code=code, collection=collection)

    @LogHistoryChange(document_type="journal", event_type="add")
    def add_journal(self, metadata):
        return self.journalmeta.add(metadata)

    @LogHistoryChange(document_type="journal", event_type="update")
    def update_journal(self, metadata):
        return self.journalmeta.update(metadata)

    def identifiers_collection(self):
        return self.collectionmeta.identifiers()

    def get_collection(self, collection):
        return self.collectionmeta.get(collection=collection)

    def collection(self, collection=None):
        """
        DEPRECATED
        """
        warnings.warn("deprecated: replaced by identifiers_collection and get_collection", DeprecationWarning)

        self.get_collection(collection=collection)

    def identifiers_journal(self, collection=None, issn=None, limit=LIMIT,
            offset=0, extra_filter=None):
        return self.journalmeta.identifiers(collection=collection, issn=issn,
                limit=limit, offset=offset, extra_filter=extra_filter)

    def identifiers_issue(self, collection=None, issn=None,
            from_date='1500-01-01', until_date=None, limit=LIMIT, offset=0,
            extra_filter=None):
        return self.issuemeta.identifiers(collection=collection, issn=issn,
                from_date=from_date, until_date=until_date, limit=limit,
                offset=offset, extra_filter=extra_filter)

    def get_issue(self, code, collection=None, replace_journal_metadata=False):
        return self.issuemeta.get(code=code, collection=collection,
                replace_journal_metadata=replace_journal_metadata)

    def get_issues_full(self, collection=None, issn=None, from_date='1500-01-01',
            until_date=None, limit=LIMIT, offset=0, extra_filter=None):
        return self.issuemeta.get_issues_full(collection=collection,
                issn=issn, from_date=from_date, until_date=until_date,
                limit=limit, offset=offset, extra_filter=extra_filter)

    def get_issues(self, code, collection=None, replace_journal_metadata=False):
        """Esse método não é utilizado em nenhum local do projeto, e tampouco
        responde por qualquer endpoint.
        """
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
        return self.journalmeta.exists(code=code, collection=collection)

    def exists_issue(self, code, collection=None):
        return self.issuemeta.exists(code=code, collection=collection)

    @LogHistoryChange(document_type="issue", event_type="delete")
    def delete_issue(self, code, collection=None):
        return self.issuemeta.delete(code=code, collection=collection)

    @LogHistoryChange(document_type="issue", event_type="add")
    def add_issue(self, metadata):
        return self.issuemeta.add(metadata)

    @LogHistoryChange(document_type="issue", event_type="update")
    def update_issue(self, metadata):
        return self.issuemeta.update(metadata)

    def identifiers_article(self,
                            collection=None,
                            issn=None,
                            from_date='1500-01-01',
                            until_date=None,
                            limit=LIMIT,
                            offset=0,
                            extra_filter=None):
        return self.articlemeta.identifiers(collection=collection, issn=issn,
                from_date=from_date, until_date=until_date, limit=limit,
                offset=offset, extra_filter=extra_filter)

    def identifiers_press_release(self,
                                  collection=None,
                                  issn=None,
                                  from_date='1500-01-01',
                                  until_date=None,
                                  limit=LIMIT,
                                  offset=0):
        return self.articlemeta.identifiers_press_release(collection=collection,
                issn=issn, from_date=from_date, until_date=until_date,
                limit=limit, offset=offset)

    def get_article(self, code, collection=None, replace_journal_metadata=False,
            body=False):
        """
            replace_journal_metadata: replace the content of the title attribute
            that cames with the article record. The content is replaced by the
            oficial and updated journal record. This may be used in cases that
            the developer intent to retrive the must recent journal data instead
            of the journal data recorded when the article was inserted in the
            collection.
        """
        return self.articlemeta.get(code=code, collection=collection,
                replace_journal_metadata=replace_journal_metadata, body=body)

    def get_articles_full(self, collection=None, issn=None,
            from_date='1500-01-01', until_date=None, limit=100, offset=0,
            extra_filter=None, replace_journal_metadata=False, body=False):
        return self.articlemeta.get_articles_full(collection=collection,
                issn=issn, from_date=from_date, until_date=until_date,
                limit=limit, offset=offset, extra_filter=extra_filter,
                replace_journal_metadata=replace_journal_metadata, body=body)

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
        return self.articlemeta.exists(code=code, collection=collection)

    @LogHistoryChange(document_type="article", event_type="delete")
    def delete_article(self, code, collection=None):
        return self.articlemeta.delete(code=code, collection=collection)

    @LogHistoryChange(document_type="article", event_type="add")
    def add_article(self, metadata):
        return self.articlemeta.add(metadata)

    @LogHistoryChange(document_type="article", event_type="update")
    def update_article(self, metadata):
        return self.articlemeta.update(metadata)

    def set_doaj_id(self, code, collection, doaj_id):
        return self.articlemeta.set_doaj_id(code=code, collection=collection,
                doaj_id=doaj_id)

    def set_aid(self, code, collection, aid):
        return self.articlemeta.set_aid(code=code, collection=collection,
                aid=aid)

    def get_issue_code_from_label(self, label, journal_code, collection):
        return self.issuemeta.get_code_from_label(label=label,
                journal_code=journal_code, collection=collection)

    def is_name_suffix(self, suffix):
        if suffix.endswith('.'):
            suffix = suffix[:-1]
        result = self.db['name_suffixes'].find_one({'suffix': suffix.lower()})
        return True if result is not None else False

    def add_name_suffix(self, metadata):
        suffix_data = {'suffix': metadata["suffix"]}
        if self.db['name_suffixes'].find(suffix_data).count() < 1:
            self.db['name_suffixes'].update_one(
                suffix_data, {'$set': suffix_data}, upsert=True
            )
