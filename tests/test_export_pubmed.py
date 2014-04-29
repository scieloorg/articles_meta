#coding: utf-8
import unittest
import xml.etree.ElementTree as ET
import json
import os

from lxml import etree
from xylose.scielodocument import Article

from articlemeta import export_pubmed
from articlemeta import export


class ExportTests(unittest.TestCase):

    def setUp(self):
        self._raw_json = json.loads(open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())
        self._article_meta = Article(self._raw_json)

    def test_xmlclose_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [None, pxml]

        xmlarticle = export_pubmed.XMLClosePipe()
        xml = xmlarticle.transform(data)

        self.assertEqual('<ArticleSet><Article /></ArticleSet>', xml)

    def test_xmljournal_pipe(self):
        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLJournalPipe()
        raw, xml = xmlarticle.transform(data)

        journal = xml.find('./Article/Journal').text

        self.assertEqual(u'Revista de Saúde Pública', journal)
