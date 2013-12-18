import json
import os
from lxml import etree

from tornado import (
    httpserver,
    httpclient,
    ioloop,
    options,
    web,
    gen
    )

from tornado.options import (
    define,
    options
    )
import tornado
import asyncmongo
import choices
from shiningdata import ShineData

define("port", default=8888, help="run on the given port", type=int)
define("mongodb_port", default=27017, help="run MongoDB on the given port", type=int)
define("mongodb_host", default='localhost', help="run MongoDB on the given hostname")
define("mongodb_database", default='scielo_network', help="Record accesses on the given database")
define("mongodb_max_connections", default=200, help="run MongoDB with the given max connections", type=int)
define("mongodb_max_cached", default=20, help="run MongoDB with the given max cached", type=int)
define("doi_prefix", default=None, help="indicates a txt file with each collection DOI prefix.", type=str)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/api/v1/article", ArticleHandler),
            (r"/api/v1/issue", IssueHandler),
            (r"/api/v1/is_loaded", IsLoadedHandler),
       ]

        self.db = asyncmongo.Client(
            pool_id='articles',
            host=options.mongodb_host,
            port=options.mongodb_port,
            maxcached=options.mongodb_max_cached,
            maxconnections=options.mongodb_max_connections,
            dbname=options.mongodb_database
        )
        self.doi_prefix = {}
        if options.doi_prefix:
            with open(options.doi_prefix) as f:
                for line in f:
                    prefix = line.split("|")
                    self.doi_prefix[prefix[0]] = prefix[1]

        self.article_types = choices.article_types

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            )

        # Local is the default the default way that ratchet works.
        tornado.web.Application.__init__(self, handlers, **settings)


class IsLoadedHandler(tornado.web.RequestHandler):

    def _remove_callback(self, response, error):
        pass

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        if len(response) > 0:
            self.write('True')
        else:
            self.write('False')
        self.finish()

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        code = self.get_argument('code')
        self.db.articles.find({"code": code}, limit=1, callback=self._on_get_response)


class IssuesHandler(tornado.web.RequestHandler):

    def callback(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        self.write(response)
        self.finish()

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.db.command('distinct', 'articles', key='code_issue', callback=self.callback)


class IssueHandler(tornado.web.RequestHandler):

    def _remove_callback(self, response, error):
        pass

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        if len(response) > 0:
            self.render('scielo.xml')

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self._is_xml = False

        def _on_response(response, error):
            if error:
                raise tornado.web.HTTPError(500)

            if len(response) > 0:
                if format == 'xml':
                    self._is_xml = True

                    shined_docs = []
                    for doc in response:
                        shined_doc = ShineData(doc,
                                                doi_prefix=self.application.doi_prefix,
                                                article_types=self.application.article_types
                                                )
                        shined_docs.append(shined_doc)

                    #import pdb; pdb.set_trace()
                    self.set_header('Content-Type', 'application/xml')
                    self.render('scielo.xml',
                        code=code,
                        docs=shined_docs
                    )
                else:
                    self.write(json.dumps(response))
                    self.finish()
            else:
                self.write('There is no data for this query!')
                self.finish()

        code = self.get_argument('code')
        format = self.get_argument('format')
        self.db.articles.find({"code_issue": code}, {"_id": 0}, callback=_on_response)

    def finish(self, chunk=None):
        if self._is_xml == True:
            try:
                p = etree.XMLParser(remove_blank_text=True)
                chunk = etree.tostring(etree.XML(chunk, parser=p))
            except:
                pass
        tornado.web.RequestHandler.finish(self, chunk)


class ArticleHandler(tornado.web.RequestHandler):

    def _remove_callback(self, response, error):
        pass

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        if len(response) > 0:
            self.render('scielo.xml')

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):
        self._method = 'post'
        code = self.get_argument('code')

        article_filename = '../isis2mongodb/output/isos/{0}/{0}_artigo.json'.format(code)
        title_filename = '../isis2mongodb/output/isos/{0}/{0}_title.json'.format(code)
        bib4cit_filename = '../isis2mongodb/output/isos/{0}/{0}_bib4cit.json'.format(code)
        article = json.loads(open(article_filename).read())
        title = json.loads(open(title_filename).read())
        bib4cit = json.loads(open(bib4cit_filename).read())

        issns = []

        applicable = 'True'
        if 'v71' in article['docs'][0]:
            # Checking if the document type is valid to be sent to WoS.
            # Some document types doesn't have metadata enough to be sent to WoS.
            if not article['docs'][0]['v71'][0]['_'] in choices.article_types:
                applicable = 'False'

        v935 = ""
        if 'v935' in title['docs'][0]:
            v935 = title['docs'][0]['v935'][0]['_']

        v400 = ""
        if 'v400' in title['docs'][0]:
            v400 = title['docs'][0]['v400'][0]['_']

        if 'v65' in article['docs'][0]:
            publication_year = article['docs'][0]['v65'][0]['_'][0:4]

        issns.append(v935)
        if v400 != v935:
            issns.append(v400)

        dict_data = {'article': article['docs'][0],
                     'title': title['docs'][0],
                     'citations': bib4cit['docs'],
                     'code_issue': code[0:18],
                     'code_title': issns,
                     'validated_scielo': 'False',
                     'validated_wos': 'False',
                     'sent_wos': 'False',
                     'publication_year': publication_year,
                     'applicable': applicable,
                    }

        self.db.articles.update(
            {'code': code},
            {'$set': dict_data},
            safe=False,
            upsert=True
        )

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self._is_xml = False
        self._method = 'get'
        self._show_citation = self.get_argument('show_citation', default=False)

        def _on_response(response, error):
            if error:
                raise tornado.web.HTTPError(500)

            show_citation = False
            if self._show_citation == 'True':
                show_citation = True

            if len(response) > 0:
                if format == 'xml':
                    self._is_xml = True
                    shined_docs = []

                    for doc in response:
                        shined_doc = ShineData(doc,
                                                doi_prefix=self.application.doi_prefix,
                                                article_types=self.application.article_types
                                                )
                        shined_docs.append(shined_doc)

                    self.set_header('Content-Type', 'application/xml')
                    self.render('scielo.xml',
                        code=code,
                        docs=shined_docs,
                        show_citation=show_citation,
                        unescape=tornado.escape.xhtml_unescape
                    )
                else:
                    self.write(json.dumps(response[0]))
                    self.finish()
            else:
                self.write('There is no data for this query!')
                self.finish()

        code = self.get_argument('code')
        format = self.get_argument('format')
        self.db.articles.find({"code": code}, {"_id": 0}, limit=1, callback=_on_response)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
