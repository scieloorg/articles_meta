#coding: utf-8
import unittest
import json
import os

import xml.etree.ElementTree as ET
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

        article = pxml.find('Article')
        article.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLPublisherNamePipe()
        raw, xml = xmlarticle.transform(data)

        publishername = xml.find('./Article/Journal/PublisherName').text

        self.assertEqual(u'Faculdade de Saúde Pública da Universidade de São Paulo', publishername)

    def test_xmljournaltitle_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        article = pxml.find('Article')
        article.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLJournalTitlePipe()
        raw, xml = xmlarticle.transform(data)

        journaltitle = xml.find('./Article/Journal/JournalTitle').text

        self.assertEqual(u'Revista de Saúde Pública', journaltitle)

    def test_xmlissn_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        article = pxml.find('Article')
        article.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLISSNPipe()
        raw, xml = xmlarticle.transform(data)

        issn = xml.find('./Article/Journal/Issn').text

        self.assertEqual(u'0034-8910', issn)

    def test_xmlvolume_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        article = pxml.find('Article')
        article.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLVolumePipe()
        raw, xml = xmlarticle.transform(data)

        volume = xml.find('./Article/Journal/Volume').text

        self.assertEqual(u'44', volume)

    def test_xmlissue_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        article = pxml.find('Article')
        article.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLIssuePipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./Article/Journal/Issue').text

        self.assertEqual(u'4', issue)

    def test_xmlpubdate_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        article = pxml.find('Article')
        article.append(ET.Element('Journal'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLPubDatePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<ArticleSet><Article><Journal><PubDate PubStatus="ppublish"><Year>2010</Year><Month>08</Month></PubDate></Journal></Article></ArticleSet>', ET.tostring(xml))

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

    def test_xmlauthorlist_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLAuthorListPipe()
        raw, xml = xmlarticle.transform(data)

        firstnames = [f.find('FirstName').text for f in xml.findall('./Article/AuthorList/Author')]
        lastnames = [l.find('LastName').text for l in xml.findall('./Article/AuthorList/Author')]

        self.assertEqual([u'Mariangela Leal',
                          u'Elaine Leandro',
                          u'Daniele Araújo Campo',
                          u'Eli Iola Gurgel',
                          u'Francisco de Assis',
                          u'Waleska Teixeira',
                          u'Ricardo',
                          u'Augusto A',
                          u'Odilon Vanni de',
                          u'Isabel Cristina'], firstnames)

        self.assertEqual([u'Cherchiglia',
                          u'Machado',
                          u'Szuster',
                          u'Andrade',
                          u'Acúrcio',
                          u'Caiaffa',
                          u'Sesso',
                          u'Guerra Junior',
                          u'Queiroz',
                          u'Gomes'], lastnames)

    def test_xmlpublicationtype_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLPublicationTypePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<ArticleSet><Article><PublicationType>research-article</PublicationType></Article></ArticleSet>', ET.tostring(xml))

    def test_xmlarticleidlist_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLArticleIDListPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<ArticleSet><Article><ArticleIdList><ArticleId IdType="pii">S0034-89102010000400007</ArticleId><ArticleId IdType="doi">10.1590/S0034-89102010000400007</ArticleId></ArticleIdList></Article></ArticleSet>', ET.tostring(xml))

    def test_xmlhistory_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))
        pxml.append(ET.Element('History'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLHistoryPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<ArticleSet><Article><History><PubDate PubStatus="accepted"><Year>2010</Year><Month>02</Month><Day>05</Day></PubDate></History></Article><History /></ArticleSet>', ET.tostring(xml))

    def test_xmlabstract_pipe(self):

        pxml = ET.Element('ArticleSet')
        pxml.append(ET.Element('Article'))

        data = [self._article_meta, pxml]

        xmlarticle = export_pubmed.XMLAbstractPipe()
        raw, xml = xmlarticle.transform(data)

        abstract = xml.find('./Article/Abstract').text[0:30]

        self.assertEqual(u'OBJETIVO: Descrever o perfil e', abstract)

    def test_validating_against_dtd(self):

        xml = etree.XML(export.Export(self._raw_json).pipeline_pubmed())

        dtd = etree.DTD(open('tests/dtd/scielo_pubmed/PubMed.dtd', 'r'))

        self.assertEqual(True, dtd.validate(xml))
