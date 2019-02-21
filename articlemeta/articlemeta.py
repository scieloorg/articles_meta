# conding: utf-8
import json
from datetime import datetime

import pyramid.httpexceptions as exc
from pyramid.view import view_config, notfound_view_config
from pyramid.response import Response
from pyramid.settings import asbool

from articlemeta.export import Export, JournalExport

DEFAULT_FROM_DATE = '1900-01-01'


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
             request_method='GET', renderer='jsonp')
def get_collection(request):

    code = request.GET.get('code', None)

    collection = request.databroker.get_collection(code)

    return collection


@view_config(route_name='identifiers_collection',
             request_method='GET', renderer='jsonp')
def identifier_collection(request):

    collections = request.databroker.identifiers_collection()

    return collections


@view_config(route_name='journal',
             request_method='GET', renderer='jsonp')
def get_journal(request):

    collection = request.GET.get('collection', None)
    issn = request.GET.get('issn', None)
    fmt = request.GET.get('format')

    journal = request.databroker.get_journal(collection=collection, issn=issn)

    if fmt == 'scieloorg':
        try:
            return JournalExport(journal[0]).pipeline_scieloorg()
        except IndexError:
            return None

    return journal


@view_config(route_name='identifiers_journal',
             request_method='GET', renderer='jsonp')
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

    return ids


@view_config(route_name='identifiers_issue',
             request_method='GET', renderer='jsonp')
def identifiers_issue(request):

    collection = request.GET.get('collection', None)
    issn = request.GET.get('issn', None)
    from_date = request.GET.get('from', DEFAULT_FROM_DATE)
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

    return ids


@view_config(route_name='exists_journal',
             request_method='GET',
             request_param=['code'], renderer='jsonp')
def exists_journal(request):

    code = request.GET.get('code', None)
    collection = request.GET.get('collection', None)

    result = request.databroker.exists_journal(code, collection=collection)

    return result

@view_config(route_name='exists_issue',
             request_method='GET',
             request_param=['code'], renderer='jsonp')
def exists_issue(request):

    code = request.GET.get('code', None)
    collection = request.GET.get('collection', None)

    issue = request.databroker.exists_issue(code, collection=collection)

    return issue


@view_config(route_name='get_issue',
             request_method='GET',
             request_param=['code'], renderer='jsonp')
def get_issue(request):

    code = request.GET.get('code', None)
    collection = request.GET.get('collection', None)

    issue = request.databroker.get_issue(
        code,
        collection=collection,
        replace_journal_metadata=True
    )

    return issue

@view_config(route_name='get_issues',
             request_method='GET', renderer='jsonp')
def get_issues(request):

    collection = request.GET.get('collection', None)
    issn = request.GET.get('issn', None)
    from_date = request.GET.get('from', DEFAULT_FROM_DATE)
    until_date = request.GET.get('until', datetime.now().date().isoformat())
    limit = _get_request_limit_param(request, default_limit=100)
    offset = request.GET.get('offset', 0)

    try:
        offset = int(offset)
    except ValueError:
        raise exc.HTTPBadRequest('offset must be integer')

    if offset < 0:
        raise exc.HTTPBadRequest('offset must be integer >= 0')

    issue = request.databroker.get_issues_full(
        collection=collection,
        issn=issn,
        limit=limit,
        offset=offset,
        from_date=from_date,
        until_date=until_date
    )

    return issue

@view_config(route_name='identifiers_article',
             request_method='GET', renderer='jsonp')
def identifiers_article(request):

    collection = request.GET.get('collection', None)
    issn = request.GET.get('issn', None)
    from_date = request.GET.get('from', DEFAULT_FROM_DATE)
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

    return ids


@view_config(route_name='identifiers_press_release',
             request_method='GET', renderer='jsonp')
def identifiers_press_release(request):

    collection = request.GET.get('collection', None)
    issn = request.GET.get('issn', None)
    from_date = request.GET.get('from', DEFAULT_FROM_DATE)
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

    return ids


@view_config(route_name='exists_article',
             request_method='GET',
             request_param=['code'], renderer='jsonp')
def exists_article(request):

    code = request.GET.get('code', None)
    collection = request.GET.get('collection', None)

    article = request.databroker.exists_article(code, collection=collection)

    return article


@view_config(route_name='get_article',
             request_method='GET',
             request_param=['code'], renderer='jsonp')
def get_article(request):

    code = request.GET.get('code', None)
    collection = request.GET.get('collection', None)
    fmt = request.GET.get('format', 'json')
    body = request.GET.get('body', 'false')

    if body not in ['true', 'false']:
        raise exc.HTTPBadRequest("parameter 'body' must be 'true' or 'false'")

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

        if fmt == 'xmlcrossref':
            return Response(
                Export(article).pipeline_crossref(), content_type="application/xml")

        if fmt == 'opac':
            return Export(article).pipeline_opac()

    return article

@view_config(route_name='get_articles',
             request_method='GET',
             renderer='jsonp')
def get_articles(request):

    collection = request.GET.get('collection', None)
    issn = request.GET.get('issn', None)
    from_date = request.GET.get('from', DEFAULT_FROM_DATE)
    until_date = request.GET.get('until', datetime.now().date().isoformat())
    limit = _get_request_limit_param(request, default_limit=100)
    offset = request.GET.get('offset', 0)
    body = request.GET.get('body', 'false')

    try:
        offset = int(offset)
    except ValueError:
        raise exc.HTTPBadRequest('offset must be integer')

    if offset < 0:
        raise exc.HTTPBadRequest('offset must be integer >= 0')

    if body not in ['true', 'false']:
        raise exc.HTTPBadRequest("parameter 'metaonly' must be 'true' or 'false', default is 'false'")

    body = asbool(body)

    articles = request.databroker.get_articles_full(
        collection=collection,
        issn=issn,
        limit=limit,
        offset=offset,
        from_date=from_date,
        until_date=until_date,
        replace_journal_metadata=True,
        body=body
    )

    return articles

@view_config(route_name='list_historychanges_article', request_method='GET', renderer='jsonp')
@view_config(route_name='list_historychanges_journal', request_method='GET', renderer='jsonp')
@view_config(route_name='list_historychanges_issue', request_method='GET', renderer='jsonp')
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
    from_date = request.GET.get('from', DEFAULT_FROM_DATE)
    until_date = request.GET.get('until', None)
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

    return objs
