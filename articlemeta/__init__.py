import os

from pyramid.renderers import JSONP
from pyramid.config import Configurator

from articlemeta import controller


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    [1]: This views are responding for requests with any methods except GET,
    so have a work-around with multiple routes path to attend with or without trailing slash.
    Reference:
    http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#redirecting-to-slash-appended-routes
    """

    config = Configurator(settings=settings)
    config.add_renderer('jsonp', JSONP(param_name='callback', indent=4))

    db_dsn = os.environ.get('MONGODB_HOST', settings.get('mongo_uri', '127.0.0.1:27017'))
    db_client = controller.get_dbconn(db_dsn)

    def add_databroker(request):
        """Add a databroker to all incoming request"""
        return controller.DataBroker(db_client)

    config.add_route('index', '/')
    # collections - GET method:
    config.add_route('collection', '/api/v1/collection/')
    config.add_route('identifiers_collection', '/api/v1/collection/identifiers/')
    # journals - GET method:
    config.add_route('journal', '/api/v1/journal/')
    config.add_route('identifiers_journal', '/api/v1/journal/identifiers/')
    config.add_route('exists_journal', '/api/v1/journal/exists/')
    # issues - GET method:
    config.add_route('get_issue', '/api/v1/issue/')
    config.add_route('get_issues', '/api/v1/issues/')
    config.add_route('identifiers_issue', '/api/v1/issue/identifiers/')
    config.add_route('exists_issue', '/api/v1/issue/exists/')
    # articles - GET method:
    config.add_route('get_article', '/api/v1/article/')
    config.add_route('get_articles', '/api/v1/articles/')
    config.add_route('identifiers_article', '/api/v1/article/identifiers/')
    config.add_route('counter_dict', '/api/v1/article/counter_dict/')
    config.add_route('exists_article', '/api/v1/article/exists/')
    # press releases - GET method:
    config.add_route('identifiers_press_release', '/api/v1/press_release/identifiers/')
    # logs historychanges - GET method:
    config.add_route('list_historychanges_article', '/api/v1/article/history/')
    config.add_route('list_historychanges_journal', '/api/v1/journal/history/')
    config.add_route('list_historychanges_issue', '/api/v1/issue/history/')
    # others
    config.add_request_method(add_databroker, 'databroker', reify=True)
    config.scan()

    return config.make_wsgi_app()
