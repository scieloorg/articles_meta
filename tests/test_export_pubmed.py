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

    def test_setuppipe_element_name(self):

        data = [None, None]

        xmlarticle = export_pubmed.SetupArticleSetPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('ArticleSet', xml.tag)

    def test_xmlarticle_pipe(self):

        pxml = ET.Element('ArticleSet')

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<ArticleSet><Article /></ArticleSet>', ET.tostring(xml))

    def test_xmljournal_pipe(self):
        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLJournalPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<ArticleSet><Article><Journal /></Article></ArticleSet>', ET.tostring(xml))

    def test_xmlpublishername_pipe(self):
        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))
        pxml.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLPublisherNamePipe()
        raw, xml = xmlarticle.transform(data)

        publishername = xml.find('./Journal/PublisherName').text

        self.assertEqual(u'Faculdade de Saúde Pública da Universidade de São Paulo', publishername)

    def test_xmljournaltitle_pipe(self):
        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))
        pxml.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLJournalTitlePipe()
        raw, xml = xmlarticle.transform(data)

        journaltitle = xml.find('./Journal/JournalTitle').text

        self.assertEqual(u'Revista de Saúde Pública', journaltitle)

    def test_xmlissn_pipe(self):
        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))
        pxml.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLISSNPipe()
        raw, xml = xmlarticle.transform(data)

        issn = xml.find('./Journal/Issn').text

        self.assertEqual(u'0034-8910', issn)

    def test_xmlvolume_pipe(self):
        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))
        pxml.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLVolumePipe()
        raw, xml = xmlarticle.transform(data)

        volume = xml.find('./Journal/Volume').text

        self.assertEqual(u'44', volume)

    def test_xmlissue_pipe(self):
        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))
        pxml.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLIssuePipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./Journal/Issue').text

        self.assertEqual(u'4', issue)

    def test_xmlpubdate_pipe(self):
        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))
        pxml.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLPubDatePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<ArticleSet><Article /><Journal><PubDate PubStatus="ppublish"><Year>2010</Year><Month>08</Month></PubDate></Journal></ArticleSet>', ET.tostring(xml))

    def test_xmlreplaces_pipe(self):
        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLReplacesPipe()
        raw, xml = xmlarticle.transform(data)

        replaces = xml.find('./Article/Replaces').text

        self.assertEqual(u'S0034-89102010000400007', replaces)

    def test_xmlarticletitle_pipe(self):
        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLArticleTitlePipe()
        raw, xml = xmlarticle.transform(data)

        articletitle = xml.find('./Article/ArticleTitle').text

        self.assertEqual(u'Perfil epidemiológico dos pacientes em terapia renal substitutiva no Brasil, 2000-2004', articletitle)

    def test_xmlfirstpage_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLFirstPagePipe()
        raw, xml = xmlarticle.transform(data)

        firstpage = xml.find('./Article/FirstPage').text

        self.assertEqual(u'639', firstpage)

    def test_xmllastpage_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLLastPagePipe()
        raw, xml = xmlarticle.transform(data)

        lastpage = xml.find('./Article/LastPage').text

        self.assertEqual(u'649', lastpage)

    def test_xmlelocatonid_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLElocationIDPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<ArticleSet><Article><ELocationID EIdType="pii">S0034-89102010000400007</ELocationID></Article></ArticleSet>', ET.tostring(xml))

    def test_xmllanguage_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLLanguagePipe()
        raw, xml = xmlarticle.transform(data)

        language = xml.find('./Article/Language').text

        self.assertEqual(u'pt', language)
