# coding: utf-8

import unittest
import xml.etree.ElementTree as ET
import json
import os

from xylose.scielodocument import Article

from articlemeta import export


class ExportTests(unittest.TestCase):

    def setUp(self):
        self._article_meta = Article(
            json.loads(
                open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read()))

    def test_xmlclosepipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        data = [None, pxml]

        xmlarticle = export.XMLClosePipe()
        xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article /></articles>', xml)

    def test_setuppipe_element_name(self):

        data = [None, None]

        xmlarticle = export.SetupPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('articles', xml.tag)

    def test_setuppipe_attributes(self):

        data = [None, None]

        xmlarticle = export.SetupPipe()
        raw, xml = xmlarticle.transform(data)

        attributes = ['xmlns:xsi',
                      'xmlns:xlink',
                      'dtd-version',
                      'xsi:noNamespaceSchemaLocation']

        self.assertEqual(attributes, xml.keys())

    def test_xmlarticlepipe(self):

        pxml = ET.Element('articles')

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article article-type="research-article" lang_id="en" /></articles>', ET.tostring(xml))

    def test_xmlfrontbackpipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        data = [None, pxml]

        xmlarticle = export.XMLFrontBackPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article><front><journal-meta /><article-meta /></front><back><ref-list /></back></article></articles>', ET.tostring(xml))

    def test_xmljournal_idpipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLJournalMetaJournalIdPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article><front><journal-meta><journal-id journal-id-type="publisher">bjoce</journal-id></journal-meta></front></article></articles>', ET.tostring(xml))

    def test_xmljournal_meta_journal_title_grouppipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLJournalMetaJournalTitleGroupPipe()
        raw, xml = xmlarticle.transform(data)

        title = xml.find('./article/front/journal-meta/journal-title-group/journal-title').text
        abbrevtitle = xml.find('./article/front/journal-meta/journal-title-group/abbrev-journal-title').text

        self.assertEqual(u'Brazilian Journal of Oceanography', title)
        self.assertEqual(u'Braz. j. oceanogr.', abbrevtitle)

