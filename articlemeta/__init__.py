from pyramid.config import Configurator
from . import controller


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    [1]: This views are responding for requests with any methods except GET,
    so have a work-around with multiple routes path to attend with or without trailing slash.
    Reference:
    http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#redirecting-to-slash-appended-routes
    """

    config = Configurator(settings=settings)

    def add_databroker(request):
        return controller.DataBroker.from_dsn(settings['mongo_uri'], reuse_dbconn=True)

    config.add_route('index', '/')
    # collections - GET method:
    config.add_route('collection', '/api/v1/collection/')
    # journals - GET method:
    config.add_route('journal', '/api/v1/journal/')
    config.add_route('identifiers_journal', '/api/v1/journal/identifiers/')
    # journals - non GET method:
    config.add_route('add_journal', '/api/v1/journal/add')
    config.add_route('add_journal_slash', '/api/v1/journal/add/')
    config.add_route('delete_journal', '/api/v1/journal/delete')
    config.add_route('delete_journal_slash', '/api/v1/journal/delete/')
    # articles - GET method:
    config.add_route('get_article', '/api/v1/article/')
    config.add_route('identifiers_article', '/api/v1/article/identifiers/')
    config.add_route('exists_article', '/api/v1/article/exists/')
    # articles - non GET method:
    config.add_route('add_article', '/api/v1/article/add')
    config.add_route('add_article_slash', '/api/v1/article/add/')
    config.add_route('update_article', '/api/v1/article/update')
    config.add_route('update_article_slash', '/api/v1/article/update/')
    config.add_route('delete_article', '/api/v1/article/delete')
    config.add_route('delete_article_slash', '/api/v1/article/delete/')
    # doaj - non GET method:
    config.add_route('set_doaj_status_true', '/api/v1/article/doaj_status_true')
    config.add_route('set_doaj_status_true_slash', '/api/v1/article/doaj_status_true/')
    config.add_route('set_doaj_status_false', '/api/v1/article/doaj_status_false')
    config.add_route('set_doaj_status_false_slash', '/api/v1/article/doaj_status_false/')
    # press releases - GET method:
    config.add_route('identifiers_press_release', '/api/v1/press_release/identifiers/')
    # logs historychanges - GET method:
    config.add_route('list_historychanges_article', '/api/v1/article/history/')
    config.add_route('list_historychanges_journal', '/api/v1/journal/history/')
    # others
    config.add_request_method(add_databroker, 'databroker', reify=True)
    config.scan()

    return config.make_wsgi_app()
