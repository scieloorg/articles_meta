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

    def test_xmlclose_pipe(self):

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

    def test_xmlarticle_pipe(self):

        pxml = ET.Element('articles')

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article article-type="research-article" lang_id="pt" /></articles>', ET.tostring(xml))

    def test_xmlfrontback_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        data = [None, pxml]

        xmlarticle = export.XMLFrontBackPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article><front><journal-meta /><article-meta /></front><back><ref-list /></back></article></articles>', ET.tostring(xml))

    def test_xmljournal_id_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLJournalMetaJournalIdPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article><front><journal-meta><journal-id journal-id-type="publisher">rsp</journal-id></journal-meta></front></article></articles>', ET.tostring(xml))

    def test_xmljournal_meta_journal_title_group_pipe(self):

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

        self.assertEqual(u'Revista de Saúde Pública', title)
        self.assertEqual(u'Rev. Saúde Pública', abbrevtitle)

    def test_xmljournal_meta_issn_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLJournalMetaISSNPipe()
        raw, xml = xmlarticle.transform(data)

        issn = xml.find('./article/front/journal-meta/issn').text

        self.assertEqual(u'0034-8910', issn)

    def test_xmljournal_meta_publisher_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLJournalMetaPublisherPipe()
        raw, xml = xmlarticle.transform(data)

        publishername = xml.find('./article/front/journal-meta/publisher/publisher-name').text
        publisherloc = xml.find('./article/front/journal-meta/publisher/publisher-loc').text

        self.assertEqual(u'Faculdade de Saúde Pública da Universidade de São Paulo', publishername)
        self.assertEqual(u'São Paulo', publisherloc)

    def test_xml_article_meta_unique_article_id_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLArticleMetaUniqueArticleIdPipe()
        raw, xml = xmlarticle.transform(data)

        uniquearticleid = xml.find('./article/front/article-meta/unique-article-id').text

        self.assertEqual(u'S0034-89102010000400007', uniquearticleid)

    def test_xml_article_meta_article_id_publisher_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLArticleMetaArticleIdPublisherPipe()
        raw, xml = xmlarticle.transform(data)

        articleidpublisher = xml.find('./article/front/article-meta/article-id[@pub-id-type="publisher-id"]').text

        self.assertEqual(u'S0034-89102010000400007', articleidpublisher)

    def test_xml_article_meta_article_id_doi_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLArticleMetaArticleIdDOIPipe()
        raw, xml = xmlarticle.transform(data)

        articleidpublisher = xml.find('./article/front/article-meta/article-id[@pub-id-type="doi"]').text

        self.assertEqual(u'10.1590/S0034-89102010000400007', articleidpublisher)

    def test_xml_article_meta_article_id_doi_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export.XMLArticleMetaArticleIdDOIPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./article/front/article-meta/article-id[@pub-id-type="doi"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xmlarticle_meta_article_categories_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLArticleMetaArticleCategoriesPipe()
        raw, xml = xmlarticle.transform(data)

        categories = [i.text for i in xml.findall('./article/front/article-meta/article-categories/subj-group/subject')]

        self.assertEqual([u'PUBLIC, ENVIRONMENTAL & OCCUPATIONAL HEALTH'], categories)

    def test_xmlarticle_meta_article_categories_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export.XMLArticleMetaArticleCategoriesPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual(None, xml.find('./article/front/article-meta/article-categories/subj-group/subject'))

    def test_xmlarticle_meta_title_group_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLArticleMetaTitleGroupPipe()
        raw, xml = xmlarticle.transform(data)

        title = xml.find('./article/front/article-meta/title-group/article-title[@lang_id="pt"]').text

        self.assertEqual(u'Perfil epidemiológico dos pacientes em terapia renal substitutiva no Brasil, 2000-2004', title)

    def test_xmlarticle_meta_translated_title_group_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        articlemeta = front.find('article-meta')
        articlemeta.append(ET.Element('title-group'))

        data = [self._article_meta, pxml]

        xmlarticle = export.XMLArticleMetaTranslatedTitleGroupPipe()
        raw, xml = xmlarticle.transform(data)

        titles = [i.find('trans-title').text for i in xml.findall('./article/front/article-meta/title-group/trans-title-group')]

        self.assertEqual([u'Epidemiological profile of patients on renal replacement therapy in Brazil, 2000-2004',
                          u'Perfil epidemiológico de los pacientes en terapia renal substitutiva en Brasil, 2000-2004'], titles)



















