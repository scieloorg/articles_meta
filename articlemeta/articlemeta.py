# conding: utf-8
import os
import urlparse
import json
from datetime import datetime

from wsgiref.simple_server import make_server
import pyramid.httpexceptions as exc
from pyramid.config import Configurator
from pyramid.view import view_config, notfound_view_config
from pyramid.response import Response
from pyramid.settings import asbool

import pymongo
import utils
import controller
from export import Export

from decorators import authenticate


def _get_request_limit_param(request, default_limit=1000,
                             only_positive_limit=True, force_max_limit_to_default=True):
    """
    Extract from request's querystring, the limit param,
    and apply some restrictions if necessary.

    @param request: the request object!
    @param default_limit: if not limit was found in querystring
    @param only_positive_limit: if true, then NOT accept limits <= 0
    @param force_max_limit_to_default: if true, then NOT accept limits > default_limit
    """

    limit = request.GET.get('limit', default_limit)
    try:
        limit = int(limit)
    except ValueError:
        raise exc.HTTPBadRequest('limit must be integer')
    else:
        if limit <= 0 and only_positive_limit:
            raise exc.HTTPBadRequest('limit must be a positive (non zero) integer')
        elif limit >= default_limit and force_max_limit_to_default:
            limit = default_limit
    return limit


@notfound_view_config(append_slash=True)
def notfound(request):
    # http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#redirecting-to-slash-appended-routes
    return exc.HTTPNotFound()


@view_config(route_name='index', request_method='GET')
def index(request):
    return Response('Articles Metadata API')


@view_config(route_name='collection',
             request_method='GET')
def get_collection(request):

    code = request.GET.get('code', None)

    collection = request.databroker.get_collection(code)

    return Response(json.dumps(collection), content_type="application/json")


@view_config(route_name='identifiers_collection',
             request_method='GET')
def identifier_collection(request):

    collections = request.databroker.identifiers_collection()

    return Response(json.dumps(collections), content_type="application/json")


@view_config(route_name='journal',
             request_method='GET')
def get_journal(request):

    collection = request.GET.get('collection', None)
    issn = request.GET.get('issn', None)

    journal = request.databroker.get_journal(collection=collection, issn=issn)

    return Response(json.dumps(journal), content_type="application/json")


@view_config(route_name='identifiers_journal',
             request_method='GET')
def identifiers_journal(request):

    collection = request.GET.get('collection', None)
    limit = _get_request_limit_param(request)
    offset = request.GET.get('offset', 0)

    try:
        offset = int(offset)
    except ValueError:
        raise exc.HTTPBadRequest('offset must be integer >= 0')

    if offset < 0:
        raise exc.HTTPBadRequest('offset must be integer >= 0')

    ids = request.databroker.identifiers_journal(collection=collection,
                                                 limit=limit,
                                                 offset=offset)

    return Response(json.dumps(ids), content_type="application/json")


@view_config(route_name='add_journal', request_method='POST')
@view_config(route_name='add_journal_slash', request_method='POST')
@authenticate
def add_journal(request):

    try:
        journal = request.databroker.add_journal(request.json_body)
    except ValueError:
        raise exc.HTTPBadRequest('The posted JSON data is not valid')

    return Response()


@view_config(route_name='delete_journal', request_method='DELETE')
@view_config(route_name='delete_journal_slash', request_method='DELETE')
@authenticate
def delete_journal(request):

    issn = request.GET.get('issn', None)
    collection = request.GET.get('collection', None)
    admintoken = request.GET.get('admintoken', None)

    if not admintoken or not issn:
        raise exc.HTTPBadRequest(
            'The attribute code and admintoken must be given'
        )

    request.databroker.delete_journal(issn, collection=collection)

    return Response()


@view_config(route_name='identifiers_issue',
             request_method='GET')
def identifiers_issue(request):

    collection = request.GET.get('collection', None)
    issn = request.GET.get('issn', None)
    from_date = request.GET.get('from', '1500-01-01')
    until_date = request.GET.get('until', datetime.now().date().isoformat())
    limit = _get_request_limit_param(request)
    offset = request.GET.get('offset', 0)

    try:
        offset = int(offset)
    except ValueError:
        raise exc.HTTPBadRequest('offset must be integer')

    if offset < 0:
        raise exc.HTTPBadRequest('offset must be integer >= 0')

    ids = request.databroker.identifiers_issue(
        collection=collection,
        issn=issn,
        limit=limit,
        offset=offset,
        from_date=from_date,
        until_date=until_date
    )

    return Response(json.dumps(ids), content_type="application/json")


@view_config(route_name='exists_issue',
             request_method='GET',
             request_param=['code'])
def exists_issue(request):

    code = request.GET.get('code', None)
    collection = request.GET.get('collection', None)

    issue = request.databroker.exists_issue(code, collection=collection)

    return Response(json.dumps(issue), content_type="application/json")


@view_config(route_name='get_issue',
             request_method='GET',
             request_param=['code'])
def get_issue(request):

    code = request.GET.get('code', None)
    collection = request.GET.get('collection', None)
    fmt = request.GET.get('format', 'json')

    issue = request.databroker.get_article(code, collection=collection)

    return Response(json.dumps(issue), content_type="application/json")


@view_config(route_name='add_issue', request_method='POST')
@view_config(route_name='add_issue_slash', request_method='POST')
@authenticate
def add_issue(request):

    try:
        issue = request.databroker.add_issue(request.json_body)
    except ValueError:
        raise exc.HTTPBadRequest('The posted JSON data is not valid')

    return Response()


@view_config(route_name='update_issue', request_method='POST')
@view_config(route_name='update_issue_slash', request_method='POST')
@authenticate
def update_article(request):

    try:
        issue = request.databroker.update_article(request.json_body)
    except ValueError:
        raise exc.HTTPBadRequest('The posted JSON data is not valid')

    return Response()


@view_config(route_name='identifiers_article',
             request_method='GET')
def identifiers_article(request):

    collection = request.GET.get('collection', None)
    issn = request.GET.get('issn', None)
    from_date = request.GET.get('from', '1500-01-01')
    until_date = request.GET.get('until', datetime.now().date().isoformat())
    limit = _get_request_limit_param(request)
    offset = request.GET.get('offset', 0)

    try:
        offset = int(offset)
    except ValueError:
        raise exc.HTTPBadRequest('offset must be integer')

    if offset < 0:
        raise exc.HTTPBadRequest('offset must be integer >= 0')

    ids = request.databroker.identifiers_article(collection=collection,
                                                 issn=issn,
                                                 limit=limit,
                                                 offset=offset,
                                                 from_date=from_date,
                                                 until_date=until_date)

    return Response(json.dumps(ids), content_type="application/json")


@view_config(route_name='identifiers_press_release',
             request_method='GET')
def identifiers_press_release(request):

    collection = request.GET.get('collection', None)
    issn = request.GET.get('issn', None)
    from_date = request.GET.get('from', '1500-01-01')
    until_date = request.GET.get('until', datetime.now().date().isoformat())
    limit = _get_request_limit_param(request)
    offset = request.GET.get('offset', 0)

    try:
        offset = int(offset)
    except ValueError:
        raise exc.HTTPBadRequest('offset must be integer')

    ids = request.databroker.identifiers_press_release(collection=collection,
                                                       issn=issn,
                                                       limit=limit,
                                                       offset=offset,
                                                       from_date=from_date,
                                                       until_date=until_date)

    return Response(json.dumps(ids), content_type="application/json")


@view_config(route_name='exists_article',
             request_method='GET',
             request_param=['code'])
def exists_article(request):

    code = request.GET.get('code', None)
    collection = request.GET.get('collection', None)

    article = request.databroker.exists_article(code, collection=collection)

    return Response(json.dumps(article), content_type="application/json")


@view_config(route_name='get_article',
             request_method='GET',
             request_param=['code'])
def get_article(request):

    code = request.GET.get('code', None)
    collection = request.GET.get('collection', None)
    fmt = request.GET.get('format', 'json')
    body = request.GET.get('body', 'false')

    if not body in ['true', 'false']:
        raise HTTPBadRequest("parameter 'metaonly' must be 'true' or 'false'")

    body = asbool(body)

    article = request.databroker.get_article(
        code, collection=collection, replace_journal_metadata=True, body=body
    )

    if article:
        if fmt == 'xmlwos':
            return Response(
                Export(article).pipeline_sci(), content_type="application/xml")

        if fmt == 'xmldoaj':
            return Response(
                Export(article).pipeline_doaj(), content_type="application/xml")

        if fmt == 'xmlrsps':
            return Response(
                Export(article).pipeline_rsps(), content_type="application/xml")

        if fmt == 'xmlpubmed':
            return Response(
                Export(article).pipeline_pubmed(), content_type="application/xml")

    return Response(json.dumps(article), content_type="application/json")


@view_config(route_name='add_article', request_method='POST')
@view_config(route_name='add_article_slash', request_method='POST')
@authenticate
def add_article(request):

    try:
        article = request.databroker.add_article(request.json_body)
    except ValueError:
        raise exc.HTTPBadRequest('The posted JSON data is not valid')

    return Response()


@view_config(route_name='update_article', request_method='POST')
@view_config(route_name='update_article_slash', request_method='POST')
@authenticate
def update_article(request):

    try:
        article = request.databroker.update_article(request.json_body)
    except ValueError:
        raise exc.HTTPBadRequest('The posted JSON data is not valid')

    return Response()


@view_config(route_name='set_doaj_status_true', request_method='POST')
@view_config(route_name='set_doaj_status_true_slash', request_method='POST')
@authenticate
def set_doaj_status_true(request):

    code = request.GET.get('code', None)

    try:
        article = request.databroker.set_doaj_status(code, True)
    except ValueError:
        raise exc.HTTPBadRequest('The posted JSON data is not valid')

    return Response()


@view_config(route_name='set_doaj_status_false', request_method='POST')
@view_config(route_name='set_doaj_status_false_slash', request_method='POST')
@authenticate
def set_doaj_status_false(request):

    code = request.GET.get('code', None)

    try:
        article = request.databroker.set_doaj_status(code, False)
    except ValueError:
        raise exc.HTTPBadRequest('The posted JSON data is not valid')

    return Response()


@view_config(route_name='delete_article', request_method='DELETE')
@view_config(route_name='delete_article_slash', request_method='DELETE')
@authenticate
def delete_article(request):

    code = request.GET.get('code', None)
    collection = request.GET.get('collection', None)

    if not code:
        raise exc.HTTPBadRequest(
            'The attribute code must be given'
        )

    token = request.registry.settings.get('app', {}).get('admintoken', None)

    request.databroker.delete_article(code, collection=collection)

    return Response()


@view_config(route_name='list_historychanges_article', request_method='GET')
@view_config(route_name='list_historychanges_journal', request_method='GET')
@view_config(route_name='list_historychanges_issue', request_method='GET')
def list_historychanges(request):
    """
    This view will attend the request from differents urls:
    - '/api/v1/article/history'
    - '/api/v1/article/history/'
    - '/api/v1/journal/history'
    - '/api/v1/journal/history/'
    - '/api/v1/issue/history'
    - '/api/v1/issue/history/'
    serving with the same logic, only difference is the type of document
    requested: 'article' or 'journal'
    """
    doc_type_by_route = {
        '/api/v1/article/history': 'article',
        '/api/v1/article/history/': 'article',
        '/api/v1/journal/history': 'journal',
        '/api/v1/journal/history/': 'journal',
        '/api/v1/issue/history': 'issue',
        '/api/v1/issue/history/': 'issue',

    }
    document_type = doc_type_by_route[request.matched_route.path]

    collection = request.GET.get('collection', None)
    event = request.GET.get('event', None)
    code = request.GET.get('code', None)
    from_date = request.GET.get('from', '1500-01-01T00:00:00')
    until_date = request.GET.get('until', datetime.now().isoformat())
    offset = request.GET.get('offset', 0)
    limit = _get_request_limit_param(request, force_max_limit_to_default=True)

    try:
        offset = int(offset)
    except ValueError:
        raise exc.HTTPBadRequest('offset must be integer')

    objs = request.databroker.historychanges(
        document_type=document_type,
        collection=collection,
        event=event,
        code=code,
        limit=limit,
        offset=offset,
        from_date=from_date,
        until_date=until_date
    )

    return Response(json.dumps(objs), content_type="application/json")
