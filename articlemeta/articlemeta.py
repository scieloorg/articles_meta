import os
import urlparse
import json

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import pymongo

import utils
import controller

@view_config(route_name='index', request_method='GET')
def index(request):
    return Response('Articles Metadata API')

@view_config(route_name='get_article', request_method='GET', request_param=['code'])
def get_article(request):

    code = request.GET.get('code', None)
    format = request.GET.get('format', 'json')

    article = request.databroker.get_article(code)

    return Response(json.dumps(article))

@view_config(route_name='add_article', request_method='POST', request_param='document')
def add_article(request):

    code = request.POST.get('document', None)

    return Response('POST: '+str(code))

def main(settings, *args, **xargs):
    config_citedby = Configurator(settings=settings)

    db_url = urlparse.urlparse(settings['app']['mongo_uri'])

    config_citedby.registry.db = pymongo.Connection(host=db_url.hostname, port=db_url.port)

    def add_collection():
        db = config_citedby.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db['articles']

    def add_databroker(request):
        return controller.DataBroker(add_collection())


    config_citedby.add_route('index', '/')
    config_citedby.add_route('get_article', '/api/v1/article')
    config_citedby.add_route('add_article', '/api/v1/article/add')
    config_citedby.add_request_method(add_databroker, 'databroker', reify=True)
    config_citedby.scan()

    return config_citedby.make_wsgi_app()

config = utils.Configuration.from_file(os.environ.get('CONFIG_INI', '../config.ini'))

settings = dict(config.items())
app = main(settings)

if __name__== '__main__':
    server = make_server(settings['http_server']['ip'], int(settings['http_server']['port']), app)
    server.serve_forever()