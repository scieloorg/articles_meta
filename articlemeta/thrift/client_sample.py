# coding: utf-8
import os
import json
import thriftpy

articlemeta_thrift = thriftpy.load(
    os.path.dirname(__file__)+'/articlemeta.thrift',
    module_name='articlemeta_thrift'
)

from thriftpy.rpc import make_client

if __name__ == '__main__':
    client = make_client(
        articlemeta_thrift.ArticleMeta,
        'localhost',
        11720
    )

    print u"Carregando 1 artigo"
    article = client.get_article('S0034-71672014000600891', collection='scl', replace_journal_metadata=True)
    identifiers = client.get_journal_identifiers(collection='scl', limit=10, offset=0)

    print u"Listando ID's de periódicos"
    for i in identifiers:
        print i.collection, i.code

    print u"Listando ID's de artigos"
    identifiers = client.get_article_identifiers(collection='scl', issn='2317-4889', limit=10, offset=0)

    for i in identifiers:
        print i.collection, i.code, i.doi, i.aid

    print u"Listando ID's de artigos com filtro extra"
    extra_filter = {'doi': '10.1590/23174889201500020002'}
    identifiers = client.get_article_identifiers(collection='scl', issn='2317-4889', extra_filter=json.dumps(extra_filter))

    for i in identifiers:
        print i.collection, i.code, i.doi, i.aid

    print u"Listando ID's de artigos com filtro extra"
    extra_filter = {'aid': {'$exists': 1}}
    identifiers = client.get_article_identifiers(collection='scl', issn='2317-4889', extra_filter=json.dumps(extra_filter))

    for i in identifiers:
        print i.collection, i.code, i.doi, i.aid
