#conding: utf-8
from xylose.scielodocument import Article
import xml.etree.ElementTree as ET
import plumber


class SetupPipe(plumber.Pipe):

    def transform(self, data):

        xml = ET.Element('articles')
        xml.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        xml.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        xml.set('xsi:noNamespaceSchemaLocation', 'ThomsonReuters_publishing_1.06.xsd')
        xml.set('dtd-version', '1.06')

        return data, xml


class XMLArticlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        xml.append(ET.Element('article'))

        return data


class XMLFrontBackPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        xml.find('article').append(ET.Element('front'))
        xml.find('article').append(ET.Element('back'))

        return data


class XMLClosePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        data = ET.tostring(xml, encoding="utf-8", method="xml")

        return data


class Export(object):

    def __init__(self, article):
        self._article = Article(article)

    def xmlwos(self):
        ppl = plumber.Pipeline(SetupPipe(), XMLArticlePipe(), XMLFrontBackPipe(), XMLClosePipe())

        transformed_data = ppl.run(self._article, rewrap=True)

        return next(transformed_data)
