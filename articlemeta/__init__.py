from pyramid.config import Configurator
from . import controller


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)

    def add_databroker(request):
        return controller.DataBroker.from_dsn(settings['mongo_uri'], reuse_dbconn=True)

    config.add_route('index', '/')
    config.add_route('collection', '/api/v1/collection')
    config.add_route('journal', '/api/v1/journal')
    config.add_route('identifiers_journal', '/api/v1/journal/identifiers')
    config.add_route('add_journal', '/api/v1/journal/add')
    config.add_route('delete_journal', '/api/v1/journal/delete')
    config.add_route('get_article', '/api/v1/article')
    config.add_route('add_article', '/api/v1/article/add')
    config.add_route('update_article', '/api/v1/article/update')
    config.add_route('set_doaj_status_true', '/api/v1/article/doaj_status_true')
    config.add_route('set_doaj_status_false', '/api/v1/article/doaj_status_false')
    config.add_route('delete_article', '/api/v1/article/delete')
    config.add_route('identifiers_article', '/api/v1/article/identifiers')
    config.add_route('identifiers_press_release', '/api/v1/press_release/identifiers')
    config.add_route('exists_article', '/api/v1/article/exists')
    config.add_request_method(add_databroker, 'databroker', reify=True)
    config.scan()

    return config.make_wsgi_app()
