# coding: utf-8
import unittest
from lxml import etree as ET
import json
import os

from lxml import etree
from xylose.scielodocument import Article

from articlemeta import export_doaj
from articlemeta import export


class ExportTests(unittest.TestCase):

    def setUp(self):
        self._raw_json = json.loads(open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())
        self._article_meta = Article(self._raw_json)

    def test_xmlclose_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [None, pxml]

        xmlarticle = export_doaj.XMLClosePipe()
        xml = xmlarticle.transform(data)

        self.assertEqual('<records><record/></records>', xml)

    def test_setuppipe_element_name(self):

        data = [None, None]

        xmlarticle = export_doaj.SetupArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('records', xml.tag)

    def test_xmlarticle_pipe(self):

        pxml = ET.Element('records')

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<records><record/></records>', ET.tostring(xml))

    def test_xmljournal_meta_journalTitlepipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLJournalMetaJournalTitlePipe()
        raw, xml = xmlarticle.transform(data)

        title = xml.find('./record/journalTitle').text

        self.assertEqual(u'Revista de Saúde Pública', title)

    def test_xmljournal_meta_issn_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLJournalMetaISSNPipe()
        raw, xml = xmlarticle.transform(data)

        issn = xml.find('./record/issn').text

        self.assertEqual(u'0034-8910', issn)

    def test_xmljournal_meta_publisher_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLJournalMetaPublisherPipe()
        raw, xml = xmlarticle.transform(data)

        publishername = xml.find('./record/publisher').text

        self.assertEqual(u'Faculdade de Saúde Pública da Universidade de São Paulo', publishername)

    def test_xml_article_meta_unique_article_id_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaIdPipe()
        raw, xml = xmlarticle.transform(data)

        uniquearticleid = xml.find('./record/publisherRecordId').text

        self.assertEqual(u'S0034-89102010000400007', uniquearticleid)

    def test_xml_article_meta_article_id_doi_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaArticleIdDOIPipe()
        raw, xml = xmlarticle.transform(data)

        articleidpublisher = xml.find('./record/doi').text

        self.assertEqual(u'10.1590/S0034-89102010000400007', articleidpublisher)

    def test_xml_article_meta_article_id_doi_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_doaj.XMLArticleMetaArticleIdDOIPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./record/doi').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xmlarticle_meta_title_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaTitlePipe()
        raw, xml = xmlarticle.transform(data)

        title = xml.find('./record/title').text

        self.assertEqual(u'Perfil epidemiológico dos pacientes em terapia renal substitutiva no Brasil, 2000-2004', title)

    def test_xmlarticle_meta_title_language_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaTitlePipe()
        raw, xml = xmlarticle.transform(data)

        title = xml.find('./record/title').get('language')

        self.assertEqual(u'pt', title)

    def test_xml_article_meta_article_id_doi_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_doaj.XMLArticleMetaArticleIdDOIPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./record/title').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xmlarticle_meta_contrib_group_author_names_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaAuthorsPipe()
        raw, xml = xmlarticle.transform(data)

        fullnames = [i.find('name').text for i in xml.findall('./record/authors/author')]

        self.assertEqual([u'Mariangela Leal Cherchiglia',
                          u'Elaine Leandro Machado',
                          u'Daniele Araújo Campo Szuster',
                          u'Eli Iola Gurgel Andrade',
                          u'Francisco de Assis Acúrcio',
                          u'Waleska Teixeira Caiaffa',
                          u'Ricardo Sesso',
                          u'Augusto A Guerra Junior',
                          u'Odilon Vanni de Queiroz',
                          u'Isabel Cristina Gomes'], fullnames)

    def test_xmlarticle_meta_contrib_group_author_xrefs_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaAuthorsPipe()
        raw, xml = xmlarticle.transform(data)

        fullnames = [i.text for i in xml.findall('./record/authors/author/affiliationId')]

        self.assertEqual([u'A01', u'A01', u'A01', u'A01', u'A01', u'A01', u'A02',
                          u'A01', u'A02', u'A01', u'A03'], fullnames)

    def test_xmlarticle_meta_contrib_group_author_without_xrefs_pipe(self):

        del(self._raw_json['article']['v71'])
        article_meta = Article(self._raw_json)

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaAuthorsPipe()
        raw, xml = xmlarticle.transform(data)

        fullnames = [i.text for i in xml.findall('./record/authors/author/affiliationId')]

        self.assertEqual([u'A01', u'A01', u'A01', u'A01', u'A01', u'A01', u'A02',
                          u'A01', u'A02', u'A01', u'A03'], fullnames)

    def test_xmlarticle_meta_contrib_group_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_doaj.XMLArticleMetaAuthorsPipe()
        raw, xml = xmlarticle.transform(data)

        try:
            xml.find('./record/authors').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xmlarticle_meta_affiliation_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_doaj.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        try:
            xml.find('./record/affiliationsList').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xmlarticle_meta_affiliation_institution_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        affiliations = [i.text for i in xml.findall('./record/affiliationsList/affiliationName')]

        self.assertEqual(sorted([u'Universidade Federal de Minas Gerais',
                          u'Universidade Federal de São Paulo',
                          u'Universidade Federal de Minas Gerais']), sorted(affiliations))

    def test_xmlarticle_meta_affiliation_index_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        indexes = [i.get('affiliationId') for i in xml.findall('./record/affiliationsList/affiliationName')]

        self.assertEqual(sorted([u'A01', u'A02', u'A03']), sorted(indexes))

    def test_xmlarticle_meta_general_info_pub_date_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaPublicationDatePipe()
        raw, xml = xmlarticle.transform(data)

        pub_year = xml.find('./record/publicationDate').text

        self.assertEqual(u'2010-08', pub_year)

    def test_xmlarticle_meta_general_info_start_page_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaStartPagePipe()
        raw, xml = xmlarticle.transform(data)

        startpage = xml.find('./record/startPage').text

        self.assertEqual(u'639', startpage)

    def test_xmlarticle_meta_general_info_start_page_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_doaj.XMLArticleMetaStartPagePipe()
        raw, xml = xmlarticle.transform(data)

        try:
            xml.find('./record/startPage').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xmlarticle_meta_general_info_end_page_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaEndPagePipe()
        raw, xml = xmlarticle.transform(data)

        startpage = xml.find('./record/endPage').text

        self.assertEqual(u'649', startpage)

    def test_xmlarticle_meta_general_info_end_page_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_doaj.XMLArticleMetaEndPagePipe()
        raw, xml = xmlarticle.transform(data)

        try:
            xml.find('./record/endPage').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xmlarticle_meta_general_info_volume_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaVolumePipe()
        raw, xml = xmlarticle.transform(data)

        startpage = xml.find('./record/volume').text

        self.assertEqual(u'44', startpage)

    def test_xmlarticle_meta_general_info_volume_without_data_pipe(self):

        del(self._article_meta.data['issue']['issue']['v31'])

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaVolumePipe()
        raw, xml = xmlarticle.transform(data)

        try:
            xml.find('./record/volume').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xmlarticle_meta_general_info_issue_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaIssuePipe()
        raw, xml = xmlarticle.transform(data)

        startpage = xml.find('./record/issue').text

        self.assertEqual(u'4', startpage)

    def test_xmlarticle_meta_general_info_issue_without_data_pipe(self):

        del(self._article_meta.data['issue']['issue']['v32'])

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaIssuePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual(xml.find('./record/issue').text, '0')

    def test_xmlarticle_meta_general_info_document_type_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaDocumentTypePipe()
        raw, xml = xmlarticle.transform(data)

        documenttype = xml.find('./record/documentType').text

        self.assertEqual(u'research-article', documenttype)

    def test_xmlarticle_meta_general_info_document_type_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_doaj.XMLArticleMetaDocumentTypePipe()
        raw, xml = xmlarticle.transform(data)

        documenttype = xml.find('./record/documentType').text

        self.assertEqual(u'undefined', documenttype)

    def test_xmlarticle_meta_general_info_fulltext_uri_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaFullTextUrlPipe()
        raw, xml = xmlarticle.transform(data)

        uri = xml.find('./record/fullTextUrl/[@format="html"]').text

        self.assertEqual(u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0034-89102010000400007&lng=en&tlng=en', uri)

    def test_xmlarticle_meta_general_info_fulltext_uri_without_data_pipe(self):

        fakexylosearticle = Article({'article': {'v65': [{'_': '201008'}]}, 'title': {}})

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_doaj.XMLArticleMetaFullTextUrlPipe()
        raw, xml = xmlarticle.transform(data)

        try:
            xml.find('./record/issue').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xmlarticle_meta_original_language_abstract_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaAbstractsPipe()
        raw, xml = xmlarticle.transform(data)

        abstract = xml.find('./record/abstract').text[0:30]

        self.assertEqual(u'OBJETIVO: Descrever o perfil e', abstract)

    def test_xmlarticle_meta_original_language_abstract_without_data_pipe(self):

        fakexylosearticle = Article({'article': {'v40': [{'_': 'pt'}]}, 'title': {}})

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_doaj.XMLArticleMetaAbstractsPipe()
        raw, xml = xmlarticle.transform(data)

        try:
            xml.find('./record/abstract').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xmlarticle_meta_keywords_languages_data_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaKeywordsPipe()
        raw, xml = xmlarticle.transform(data)

        keywords_language = [i.get('language') for i in xml.findall('./record/keywords')]

        self.assertEqual([u'en', u'es', u'pt'], keywords_language)

    def test_xmlarticle_meta_keywords_pipe(self):

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [self._article_meta, pxml]

        xmlarticle = export_doaj.XMLArticleMetaKeywordsPipe()
        raw, xml = xmlarticle.transform(data)

        keywords = [i.text for i in xml.findall('./record/keywords/keyword')]

        self.assertEqual([u'Renal Insufficiency, Chronic',
                          u'Renal Replacement Therapy',
                          u'Hospital Information Systems',
                          u'Mortality Registries',
                          u'Insuficiencia Renal Crónica',
                          u'Terapia de Reemplazo Renal',
                          u'Sistemas de Información en Hospital',
                          u'Registros de Mortalidad',
                          u'Insuficiência Renal Crônica',
                          u'Terapia de Substituição Renal',
                          u'Sistemas de Informação Hospitalar',
                          u'Registros de Mortalidade'], keywords)

    def test_xmlarticle_meta_keywords_without_data_pipe(self):

        fakexylosearticle = Article({'article': {'v40': [{'_': 'pt'}]}, 'title': {}})

        pxml = ET.Element('records')
        pxml.append(ET.Element('record'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_doaj.XMLArticleMetaKeywordsPipe()
        raw, xml = xmlarticle.transform(data)

        try:
            xml.find('./record/keywords').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_validating_against_schema(self):

        xml = export.Export(self._raw_json).pipeline_doaj()

        xsd = open('tests/xsd/scielo_doaj/doajArticles.xsd', 'r').read()
        schema_root = etree.XML(xsd)

        schema = etree.XMLSchema(schema_root)
        xmlparser = etree.XMLParser(schema=schema)

        expected = etree.fromstring(xml, xmlparser).tag

        self.assertEqual('records', expected)
