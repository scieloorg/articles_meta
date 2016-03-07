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
        'articlemeta.scielo.org',
        11720
    )

    print u"Carregando 1 artigo"
    article = client.get_article('S0034-71672014000600891', collection='scl', replace_journal_metadata=True)
    print json.loads(article)['code']

    print u"Listando ID's de periódicos"
    identifiers = client.get_journal_identifiers(collection='scl', limit=10, offset=0)
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
    identifiers = client.get_article_identifiers(collection='scl', issn='0103-4979', extra_filter=json.dumps(extra_filter))

    for i in identifiers:
        print i.collection, i.code, i.doi, i.aid

    print u"Listando ID's de issues"
    identifiers = client.get_issue_identifiers(collection='scl', issn='0103-4979', limit=10, offset=0)

    for i in identifiers:
        print i.collection, i.code

    print u"Listando ID's de issues com filtro extra"
    extra_filter = {'issue_type': 'special'}
    identifiers = client.get_issue_identifiers(collection='scl', issn='0103-4979', extra_filter=json.dumps(extra_filter))

    for i in identifiers:
        print i.collection, i.code

    print u"Recuperando um issues"
    issue = client.get_issue(code='0103-733120080004', collection='scl')

    print issue