# coding: utf-8
import unittest
import xml.etree.ElementTree as ET
import json
import os

from lxml import etree
from xylose.scielodocument import Article

from articlemeta import export_iahx
from articlemeta import export


class ExportTests(unittest.TestCase):

    def setUp(self):
        self._raw_json = json.loads(open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())
        self._article_meta = Article(self._raw_json)

    def test_setuppipe_element_name(self):

        data = [self._article_meta, None]

        xmlarticle = export_iahx.SetupDocumentPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<doc />', ET.tostring(xml))

    def test_xml_document_id_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLDocumentIDPipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="id"]').text

        self.assertEqual(u'art-S0034-89102010000400007-scl', result)

    def test_xml_document_collection_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLCollectionPipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="in"]').text

        self.assertEqual(u'scl', result)

    def test_xml_document_knowledge_area_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLKnowledgeAreaPipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="ac"]').text

        self.assertEqual(u'Health Sciences', result)

    def test_xml_document_doi_data_pipe(self):

        fakexylosearticle = Article({'title': {}, 'doi': 'http://dx.doi.org/10.1590/s0036-36342011000900009'})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLDOIPipe()

        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="doi"]').text

        self.assertEqual(u'10.1590/S0036-36342011000900009', result)

    def test_xml_document_doi_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLDOIPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="doi"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_knowledge_area_multiple_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {'v441': [{'_': 'Health Sciences'}, {'_': 'Human Sciences'}]}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLKnowledgeAreaPipe()

        raw, xml = xmlarticle.transform(data)

        result = ', '.join([ac.text for ac in xml.findall('./field[@name="ac"]')])

        self.assertEqual(u'Health Sciences, Human Sciences', result)

    def test_xml_document_knowledge_area_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLKnowledgeAreaPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="ac"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_center_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLCenterPipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="cc"]').text

        self.assertEqual(u'br1.1', result)

    def test_xml_document_type_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLDocumentTypePipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="type"]').text

        self.assertEqual(u'research-article', result)

    def test_xml_document_ur_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLURPipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="ur"]').text

        self.assertEqual(u'art-S0034-89102010000400007', result)

    def test_xml_document_authors_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLAuthorsPipe()
        raw, xml = xmlarticle.transform(data)

        result = '; '.join([ac.text for ac in xml.findall('./field[@name="au"]')])

        self.assertEqual(u'Mariangela Leal, Cherchiglia; Elaine Leandro, Machado; Daniele Ara\xfajo Campo, Szuster; Eli Iola Gurgel, Andrade; Francisco de Assis, Ac\xfarcio; Waleska Teixeira, Caiaffa; Ricardo, Sesso; Augusto A, Guerra Junior; Odilon Vanni de, Queiroz; Isabel Cristina, Gomes', result)

    def test_xml_document_authors_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLAuthorsPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="au"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_title_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLTitlePipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="ti_pt"]').text[0:20]
        self.assertEqual(u'Perfil epidemiológic', result)

        result = xml.find('./field[@name="ti_en"]').text[0:20]
        self.assertEqual(u'Epidemiological prof', result)

        result = xml.find('./field[@name="ti_es"]').text[0:20]
        self.assertEqual(u'Perfil epidemiológic', result)

    def test_xml_document_title_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLTitlePipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="ti"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_pages_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLPagesPipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="pg"]').text

        self.assertEqual(u'639-649', result)

    def test_xml_document_pages_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLPagesPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="pg"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_wok_citation_index_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLWOKCIPipe()
        raw, xml = xmlarticle.transform(data)

        result = ', '.join([i.text for i in xml.findall('./field[@name="wok_citation_index"]')])

        self.assertEqual(u'SCIE, SSCI', result)

    def test_xml_document_wok_citation_index_AHCI_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {'v853': [{'_': 'A&HCI'}]}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLWOKCIPipe()
        raw, xml = xmlarticle.transform(data)

        result = ', '.join([i.text for i in xml.findall('./field[@name="wok_citation_index"]')])

        self.assertEqual(u'AHCI', result)

    def test_xml_document_wok_citation_index_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLWOKCIPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="wok_citation_index"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_wok_subject_categories_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLWOKSCPipe()
        raw, xml = xmlarticle.transform(data)

        result = ', '.join([i.text for i in xml.findall('./field[@name="wok_subject_categories"]')])

        self.assertEqual(u'PUBLIC, ENVIRONMENTAL & OCCUPATIONAL HEALTH', result)

    def test_xml_document_multiple_wok_subject_categories_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {'v854': [{'_': 'Cat 1'}, {'_': 'Cat 2'}]}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLWOKSCPipe()
        raw, xml = xmlarticle.transform(data)

        result = ', '.join([i.text for i in xml.findall('./field[@name="wok_subject_categories"]')])

        self.assertEqual(u'Cat 1, Cat 2', result)

    def test_xml_document_wok_subject_categories_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('add')
        pxml.append(ET.Element('doc'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLWOKSCPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="wok_subject_categories"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_issue_label_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLIssueLabelPipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="fo"]').text

        self.assertEqual(u'Rev. Saúde Pública; 44(4); 639-649; 2010-08', result)

    def test_xml_document_journal_title_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLJournalTitlePipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="journal_title"]').text

        self.assertEqual(u'Revista de Saúde Pública', result)

    def test_xml_document_journal_abbrev_title_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLJournalAbbrevTitlePipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="ta"]').text

        self.assertEqual(u'Rev. Saúde Pública', result)

    def test_xml_document_available_languages_pipe(self):

        pxml = ET.Element('doc')
        pxml.append(ET.Element('doc'))

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLAvailableLanguagesPipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="la"]').text

        self.assertEqual(u'pt', result)

    def test_xml_document_available_languages_pipe(self):

        pxml = ET.Element('doc')
        pxml.append(ET.Element('doc'))

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLAvailableLanguagesPipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="la"]').text

        self.assertEqual(u'pt', result)

    def test_xml_document_available_languages_plus_fulltexts_pipe(self):

        pxml = ET.Element('doc')
        pxml.append(ET.Element('doc'))

        self._article_meta.data['fulltexts'] = {
            'pdf': {
                'en': 'url_pdf_en',
            },
            'html': {
                'en': 'url_html_en',
            },            
        }
        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLAvailableLanguagesPipe()
        raw, xml = xmlarticle.transform(data)

        result = sorted([i.text for i in xml.findall('./field[@name="la"]')])

        self.assertEqual([u'en', u'pt'], result)

    def test_xml_document_publication_date_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLPublicationDatePipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="da"]').text

        self.assertEqual(u'2010-08', result)

    def test_xml_document_abstract_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLAbstractPipe()
        raw, xml = xmlarticle.transform(data)

        result = xml.find('./field[@name="ab_pt"]').text[0:20]
        self.assertEqual(u'OBJETIVO: Descrever ', result)

        result = xml.find('./field[@name="ab_en"]').text[0:20]
        self.assertEqual(u'OBJECTIVE: To descri', result)

        result = xml.find('./field[@name="ab_es"]').text[0:20]
        self.assertEqual(u'OBJETIVO: Describir ', result)

    def test_xml_document_affiliation_country_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLAffiliationCountryPipe()
        raw, xml = xmlarticle.transform(data)

        result = [i.text for i in xml.findall('./field[@name="aff_country"]')]

        self.assertEqual(['BRAZIL'], result)

    def test_xml_document_affiliation_country_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLAffiliationCountryPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="aff_country"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_affiliation_institution_pipe(self):

        pxml = ET.Element('doc')
        pxml.append(ET.Element('doc'))

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLAffiliationInstitutionPipe()
        raw, xml = xmlarticle.transform(data)

        result = [i.text for i in xml.findall('./field[@name="aff_institution"]')]

        self.assertEqual(
            sorted([u'Universidade Federal de Minas Gerais', u'Universidade Federal de São Paulo']),
            sorted(result)
        )

    def test_xml_document_affiliation_institution_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLAffiliationInstitutionPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="aff_institution"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_document_sponsor_pipe(self):

        pxml = ET.Element('doc')

        data = [self._article_meta, pxml]

        xmlarticle = export_iahx.XMLSponsorPipe()
        raw, xml = xmlarticle.transform(data)

        result = [i.text for i in xml.findall('./field[@name="sponsor"]')]

        self.assertEqual([u'Fundação de Amparo à Pesquisa do Estado de Minas Gerais', u'Ministério da Saúde', u'Conselho Nacional de Desenvolvimento Científico e Tecnológico'], result)


    def test_xml_document_sponsor_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('doc')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_iahx.XMLSponsorPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./field[name="sponsor"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
