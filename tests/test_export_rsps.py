# coding: utf-8
import unittest
from lxml import etree as ET
import json
import os

from lxml import etree
from xylose.scielodocument import Article

from articlemeta import export_rsps
from articlemeta import export


class XMLCitationTests(unittest.TestCase):

    def setUp(self):

        self._raw_json = json.loads(open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())
        self._citation_meta = Article(self._raw_json).citations[0]

        self._xmlcitation = export_rsps.XMLCitation()

    def test_xml_citation_setup_pipe(self):

        data = [self._citation_meta, None]

        raw, xml = self._xmlcitation.SetupCitationPipe().transform(data)

        rootcitation = xml.findall('.')[0].tag

        self.assertEqual('ref', rootcitation)

    def test_xml_citation_id_as_str_pipe(self):

        pxml = ET.Element('ref')

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.RefIdPipe().transform(data)

        strid = xml.find('.').get('id')

        self.assertTrue(isinstance(strid, str))

    def test_xml_citation_element_citation_pipe(self):

        pxml = ET.Element('ref')

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.ElementCitationPipe().transform(data)

        publicationtype = xml.find('./element-citation[@publication-type="journal"]').get('publication-type')

        self.assertEqual(u'journal', publicationtype)

    def test_xml_citation_article_title_pipe(self):

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.ArticleTitlePipe().transform(data)

        expected = xml.find('./element-citation/article-title').text

        self.assertEqual(u'End-stage renal disease in sub-Saharan Africa.', expected)

    def test_xml_citation_article_title_without_data_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.ArticleTitlePipe().transform(data)

        expected = xml.find('./element-citation/article-title')

        self.assertEqual(None, expected)

    def test_xml_citation_source_pipe(self):

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.SourcePipe().transform(data)

        expected = xml.find('./element-citation/source').text

        self.assertEqual(u'Ethn Dis.', expected)

    def test_xml_citation_source_without_data_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.SourcePipe().transform(data)

        expected = xml.find('./element-citation/source')

        self.assertEqual(None, expected)

    def test_xml_citation_date_pipe(self):

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.DatePipe().transform(data)

        expected = xml.find('./element-citation/date/year').text

        self.assertEqual(u'2006', expected)

    def test_xml_citation_date_with_year_and_month_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{'v65': [{'_': '200604'}]}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.DatePipe().transform(data)

        expected_year = xml.find('./element-citation/date/year').text
        expected_month = xml.find('./element-citation/date/month').text

        self.assertEqual(u'2006', expected_year)
        self.assertEqual(u'04', expected_month)

    def test_xml_citation_date_with_year_and_month_and_day_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{'v65': [{'_': '20060430'}]}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.DatePipe().transform(data)

        expected_year = xml.find('./element-citation/date/year').text
        expected_month = xml.find('./element-citation/date/month').text
        expected_day = xml.find('./element-citation/date/day').text

        self.assertEqual(u'2006', expected_year)
        self.assertEqual(u'04', expected_month)
        self.assertEqual(u'30', expected_day)

    def test_xml_citation_date_without_data_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.DatePipe().transform(data)

        expected = xml.find('./element-citation/date')

        self.assertEqual(None, expected)

    def test_xml_citation_fpage_pipe(self):

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.StartPagePipe().transform(data)

        expected = xml.find('./element-citation/fpage').text

        self.assertEqual(u'2,5,9', expected)

    def test_xml_citation_fpage_without_data_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.StartPagePipe().transform(data)

        expected = xml.find('./element-citation/fpage')

        self.assertEqual(None, expected)

    def test_xml_citation_lpage_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{'v14': [{'_': '120-130'}]}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.EndPagePipe().transform(data)

        expected = xml.find('./element-citation/lpage').text

        self.assertEqual(u'130', expected)

    def test_xml_citation_lpage_without_data_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.EndPagePipe().transform(data)

        expected = xml.find('./element-citation/lpage')

        self.assertEqual(None, expected)

    def test_xml_citation_volume_pipe(self):

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.VolumePipe().transform(data)

        expected = xml.find('./element-citation/volume').text

        self.assertEqual(u'16', expected)

    def test_xml_citation_volume_without_data_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.VolumePipe().transform(data)

        expected = xml.find('./element-citation/volume')

        self.assertEqual(None, expected)

    def test_xml_citation_issue_pipe(self):

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.IssuePipe().transform(data)

        expected = xml.find('./element-citation/issue').text

        self.assertEqual(u'2', expected)

    def test_xml_citation_issue_without_data_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.IssuePipe().transform(data)

        expected = xml.find('./element-citation/issue')

        self.assertEqual(None, expected)

    def test_xml_citation_person_group_len_pipe(self):

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.PersonGroupPipe().transform(data)

        expected = len(xml.findall('./element-citation/person-group/name'))

        self.assertEqual(1, expected)

    def test_xml_citation_person_group_given_names_pipe(self):

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.PersonGroupPipe().transform(data)

        result = xml.find('./element-citation/person-group[@person-group-type="author"]/name/given-names').text

        self.assertEqual('EL', result)

    def test_xml_citation_person_group_surname_pipe(self):

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.PersonGroupPipe().transform(data)

        result = xml.find('./element-citation/person-group[@person-group-type="author"]/name/surname').text

        self.assertEqual('Bamgboye', result)

    def test_xml_citation_person_group_without_data_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.PersonGroupPipe().transform(data)

        expected = xml.find('./element-citation/person-group')

        self.assertEqual(None, expected)


class ExportTests(unittest.TestCase):

    def setUp(self):
        self._raw_json = json.loads(open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())
        self._article_meta = Article(self._raw_json)

    def test_xmlclose_pipe(self):

        pxml = ET.Element('article')

        data = [None, pxml]

        xmlarticle = export_rsps.XMLClosePipe()
        xml = xmlarticle.transform(data)

        self.assertEqual('<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">\n<article/>'.encode('utf-8'), xml)

    def test_setuppipe_element_name(self):

        data = [None, None]

        xmlarticle = export_rsps.SetupArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('article', xml.tag)

    def test_setuppipe_attributes_specific_use(self):

        data = [None, None]

        xmlarticle = export_rsps.SetupArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertTrue('sps-1.1', xml.find('.').get('specific-use'))

    def test_setuppipe_attributes_dtd_version(self):

        data = [None, None]

        xmlarticle = export_rsps.SetupArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertTrue('1.0', xml.find('.').get('dtd-version'))

    def test_xmlarticle_pipe(self):

        pxml = ET.Element('article')

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<article xml:lang="pt" article-type="research-article"/>'.encode('utf-8'), ET.tostring(xml))

    def test_xmlfront_pipe(self):

        pxml = ET.Element('article')

        data = [None, pxml]

        xmlarticle = export_rsps.XMLFrontPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<article><front><journal-meta/><article-meta/></front></article>'.encode('utf-8'), ET.tostring(xml))

    def test_xmljournal_id_pipe(self):

        pxml = ET.Element('article')

        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLJournalMetaJournalIdPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<article><front><journal-meta><journal-id journal-id-type="publisher-id">rsp</journal-id></journal-meta></front></article>'.encode('utf-8'), ET.tostring(xml))

    def test_xmljournal_meta_journal_title_group_pipe(self):

        pxml = ET.Element('article')

        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLJournalMetaJournalTitleGroupPipe()
        raw, xml = xmlarticle.transform(data)

        title = xml.find('./front/journal-meta/journal-title-group/journal-title').text

        self.assertEqual(u'Revista de Saúde Pública', title)

    def test_xmljournal_meta_abbrev_journal_title_pipe(self):

        pxml = ET.Element('article')

        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLJournalMetaJournalTitleGroupPipe()
        raw, xml = xmlarticle.transform(data)

        abbrevtitle = xml.find('./front/journal-meta/journal-title-group/abbrev-journal-title').text

        self.assertEqual(u'Rev. Saúde Pública', abbrevtitle)

    def test_xmljournal_meta_abbrev_journal_title_pipe(self):

        pxml = ET.Element('article')

        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLJournalMetaJournalTitleGroupPipe()
        raw, xml = xmlarticle.transform(data)

        abbrevtype = xml.find('./front/journal-meta/journal-title-group/abbrev-journal-title').get('abbrev-type')

        self.assertEqual(u'publisher', abbrevtype)

    def test_xmljournal_meta_print_issn_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLJournalMetaISSNPipe()
        raw, xml = xmlarticle.transform(data)

        issn = xml.find('./front/journal-meta/issn[@pub-type="ppub"]').text

        self.assertEqual(u'0034-8910', issn)

    def test_xmljournal_meta_electronic_issn_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('journal-meta'))

        self._article_meta.data['title']['v400'][0]['_'] = 'XXXX-XXXX'

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLJournalMetaISSNPipe()

        raw, xml = xmlarticle.transform(data)

        issn = xml.find('./front/journal-meta/issn[@pub-type="epub"]').text

        self.assertEqual(u'XXXX-XXXX', issn)

    def test_xmljournal_meta_publisher_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLJournalMetaPublisherPipe()
        raw, xml = xmlarticle.transform(data)

        publishername = xml.find('./front/journal-meta/publisher/publisher-name').text
        publisherloc = xml.find('./front/journal-meta/publisher/publisher-loc').text

        self.assertEqual(u'Faculdade de Saúde Pública da Universidade de São Paulo', publishername)
        self.assertEqual(u'São Paulo, SP, Brazil', publisherloc)

    def test_xml_article_meta_article_id_publisher_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaArticleIdPublisherPipe()
        raw, xml = xmlarticle.transform(data)

        articleidpublisher = xml.find('./front/article-meta/article-id[@pub-id-type="publisher-id"]').text

        self.assertEqual(u'S0034-89102010000400007', articleidpublisher)

    def test_xml_article_meta_article_id_doi_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaArticleIdDOIPipe()
        raw, xml = xmlarticle.transform(data)

        articleidpublisher = xml.find('./front/article-meta/article-id[@pub-id-type="doi"]').text

        self.assertEqual(u'10.1590/S0034-89102010000400007', articleidpublisher)

    def test_xml_article_meta_article_id_doi_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLArticleMetaArticleIdDOIPipe()

        raw, xml = xmlarticle.transform(data)

        # This try except is a trick to test the expected result of the
        # piped XML, once the precond method don't raise an exception
        # we try to check if the preconditioned pipe was called or not.
        try:
            xml.find('./front/article-meta/article-id[@pub-id-type="doi"]').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xml_article_body_without_data_pipe(self):

        fakexylosearticle = Article({'article': {'v40': [{'_': 'pt'}]}, 'title': {}, 'body': {'pt': 'body pt', 'es': 'body es'}})

        pxml = ET.Element('article')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLBodyPipe()

        raw, xml = xmlarticle.transform(data)

        body = xml.find('./body/p').text

        self.assertEqual('body pt', body)

    def test_xml_article_body_without_data_pipe(self):

        fakexylosearticle = Article({'article': {'v40': [{'_': 'pt'}]}, 'title': {}})

        pxml = ET.Element('article')

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLBodyPipe()

        raw, xml = xmlarticle.transform(data)

        try:
            xml.find('./body/p').text
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_xmlarticle_meta_article_categories_pipe(self):

        fakexylosearticle = Article({'article': {'v40': [{'_': 'pt'}]}, 'section': {u'pt': u'label pt', u'es': u'label es'}})

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLArticleMetaArticleCategoriesPipe()
        raw, xml = xmlarticle.transform(data)

        categories = xml.find('./front/article-meta/article-categories/subj-group[@subj-group-type="heading"]/subject').text

        self.assertEqual(u'label pt', categories)

    def test_xmlarticle_meta_article_categories_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLArticleMetaArticleCategoriesPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual(None, xml.find('./front/article-meta/article-categories/subj-group/subject'))

    def test_xmlarticle_meta_title_group_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaTitleGroupPipe()
        raw, xml = xmlarticle.transform(data)

        title = xml.find('./front/article-meta/title-group/article-title').text

        self.assertEqual(u'Perfil epidemiológico dos pacientes em terapia renal substitutiva no Brasil, 2000-2004', title)

    def test_xmlarticle_meta_translated_title_group_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        articlemeta = front.find('article-meta')
        articlemeta.append(ET.Element('title-group'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaTranslatedTitleGroupPipe()
        raw, xml = xmlarticle.transform(data)

        titles = [i.find('trans-title').text for i in xml.findall('./front/article-meta/title-group/trans-title-group')]

        self.assertEqual([u'Perfil epidemiológico de los pacientes en terapia renal substitutiva en Brasil, 2000-2004'], titles)

    def test_xmlarticle_meta_translated_title_group_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        articlemeta = front.find('article-meta')
        articlemeta.append(ET.Element('title-group'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        titles = [i.find('trans-title').text for i in xml.findall('./front/article-meta/title-group/trans-title-group')]

        self.assertEqual([], titles)

    def test_xmlarticle_meta_contrib_group_author_names_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        fullnames = [' '.join([i.find('given-names').text, i.find('surname').text]) for i in xml.findall('./front/article-meta/contrib-group/contrib/name')]

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

    def test_xmlarticle_meta_contrib_group_author_roles_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        fullnames = [i.text for i in xml.findall('./front/article-meta/contrib-group/contrib/role')]

        self.assertEqual([u'ND', u'ND', u'ND', u'ND', u'ND', u'ND', u'ND',
                          u'ND', u'ND', u'ND'], fullnames)

    def test_xmlarticle_meta_contrib_group_author_xrefs_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        fullnames = [i.get('rid') for i in xml.findall('./front/article-meta/contrib-group/contrib/xref')]

        self.assertEqual([u'aff01', u'aff01', u'aff01', u'aff01', u'aff01', u'aff01', u'aff02',
                          u'aff01', u'aff02', u'aff01', u'aff03'], fullnames)

    def test_xmlarticle_meta_contrib_group_author_without_xrefs_pipe(self):

        del(self._raw_json['article']['v71'])
        article_meta = Article(self._raw_json)

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        fullnames = [i.get('rid') for i in xml.findall('./front/article-meta/contrib-group/contrib/xref')]

        self.assertEqual([u'aff01', u'aff01', u'aff01', u'aff01', u'aff01', u'aff01', u'aff02',
                          u'aff01', u'aff02', u'aff01', u'aff03'], fullnames)

    def test_xmlarticle_meta_contrib_group_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        titles = [i.find('contrib-group').text for i in xml.findall('./front/article-meta/contrib-group/contrib')]

        self.assertEqual([], titles)

    def test_xmlarticle_meta_affiliation_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        affiliations = [i.find('institution').text for i in xml.findall('./front/article-meta/aff')]

        self.assertEqual([], affiliations)

    def test_xmlarticle_meta_affiliation_institution_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        affiliations = sorted([i.find('institution').text for i in xml.findall('./front/article-meta/aff')])

        self.assertEqual(sorted([u'Universidade Federal de Minas Gerais',
                          u'Universidade Federal de São Paulo',
                          u'Universidade Federal de Minas Gerais']), affiliations)

    def test_xmlarticle_meta_affiliation_index_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        indexes = sorted([i.get('id') for i in xml.findall('./front/article-meta/aff')])

        self.assertEqual(sorted([u'aff01',
                          u'aff02',
                          u'aff03']), indexes)

    def test_xmlarticle_meta_affiliation_country_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        countries = [i.find('country').text for i in xml.findall('./front/article-meta/aff')]

        self.assertEqual([u'BRAZIL',
                          u'BRAZIL',
                          u'BRAZIL'], countries)

    def test_xmlarticle_meta_affiliation_address_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        address = sorted([i.text for i in xml.findall('./front/article-meta/aff/addr-line/named-content[@content-type="city"]')])

        self.assertEqual(sorted([u'Belo Horizonte',
                          u'São Paulo',
                          u'Belo Horizonte']), address)

    def test_xmlarticle_meta_general_info_pub_year_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaDatesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        pub_year = xml.find('./front/article-meta/pub-date[@pub-type="epub-ppub"]/year').text

        self.assertEqual(u'2010', pub_year)

    def test_xmlarticle_meta_general_info_pub_month_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaDatesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        pub_month = xml.find('./front/article-meta/pub-date/month').text

        self.assertEqual(u'08', pub_month)

    def test_xmlarticle_meta_general_info_elocation_pipe(self):

        self._article_meta.data['article']['v14'][0]['e'] = 'eloc1'

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaElocationInfoPipe()
        raw, xml = xmlarticle.transform(data)

        eloc = xml.find('./front/article-meta/elocation-id').text

        self.assertEqual(u'eloc1', eloc)

    def test_xmlarticle_meta_general_info_without_elocation_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaElocationInfoPipe()
        raw, xml = xmlarticle.transform(data)

        eloc = xml.find('./front/article-meta/elocation-id')

        self.assertEqual(None, eloc)

    def test_xmlarticle_meta_general_info_first_page_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaPagesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        fpage = xml.find('./front/article-meta/fpage').text

        self.assertEqual(u'639', fpage)

    def test_xmlarticle_meta_general_info_without_first_page_pipe(self):

        del(self._article_meta.data['article']['v14'][0]['f'])

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaPagesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        fpage = xml.find('./front/article-meta/fpage')

        self.assertEqual(None, fpage)

    def test_xmlarticle_meta_general_info_last_page_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaPagesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        lpage = xml.find('./front/article-meta/lpage').text

        self.assertEqual(u'649', lpage)

    def test_xmlarticle_meta_general_info_without_last_page_pipe(self):

        del(self._article_meta.data['article']['v14'][0]['l'])

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaPagesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        lpage = xml.find('./front/article-meta/lpage')

        self.assertEqual(None, lpage)

    def test_xmlarticle_meta_general_info_volume_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        volume = xml.find('./front/article-meta/volume').text

        self.assertEqual(u'44', volume)

    def test_xmlarticle_meta_general_info_without_volume_pipe(self):

        del(self._article_meta.data['issue']['issue']['v31'])

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertIsNone(xml.find('./front/article-meta/volume'))

    def test_xmlarticle_meta_general_info_issue_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./front/article-meta/issue').text

        self.assertEqual(u'4', issue)

    def test_xmlarticle_meta_general_info_without_issue_pipe(self):

        del(self._article_meta.data['issue']['issue']['v32'])

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertIsNone(xml.find('./front/article-meta/issue'))

    def test_xmlarticle_meta_general_info_suppl_vol_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        del(self._article_meta.data['issue']['issue']['v32'])
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '1'}]

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./front/article-meta/issue').text

        self.assertEqual(u'suppl 1', issue)

    def test_xmlarticle_meta_general_info_suppl_vol_0_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        del(self._article_meta.data['issue']['issue']['v32'])
        self._article_meta.data['issue']['issue']['v31'] = [{'_': '10'}]
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '0'}]

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./front/article-meta/issue').text

        self.assertEqual(u'suppl', issue)

    def test_xmlarticle_meta_general_info_suppl_issue_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        self._article_meta.data['issue']['issue']['v31'] = [{'_': '10'}]
        self._article_meta.data['issue']['issue']['v32'] = [{'_': '1'}]
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '2'}]

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./front/article-meta/issue').text

        self.assertEqual(u'1 suppl 2', issue)

    def test_xmlarticle_meta_general_info_suppl__vol_10_issue_1_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        self._article_meta.data['issue']['issue']['v31'] = [{'_': '10'}]
        self._article_meta.data['issue']['issue']['v32'] = [{'_': '1'}]
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '0'}]

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./front/article-meta/issue').text

        self.assertEqual(u'1 suppl', issue)

    def test_xmlarticle_meta_general_info_suppl__vol_10_issue_20_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        self._article_meta.data['issue']['issue']['v31'] = [{'_': '10'}]
        self._article_meta.data['issue']['issue']['v32'] = [{'_': '20'}]
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '0'}]

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./front/article-meta/issue').text

        self.assertEqual(u'20 suppl', issue)

    def test_xmlarticle_meta_general_info_suppl__vol_10_issue_20_suppl_10_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        self._article_meta.data['issue']['issue']['v31'] = [{'_': '10'}]
        self._article_meta.data['issue']['issue']['v32'] = [{'_': '20'}]
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '10'}]

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./front/article-meta/issue').text

        self.assertEqual(u'20 suppl 10', issue)

    def test_xmlarticle_meta_original_language_abstract_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaAbstractsPipe()
        raw, xml = xmlarticle.transform(data)

        abstract = xml.find('./front/article-meta/abstract/p').text[0:30]

        self.assertEqual(u'OBJETIVO: Descrever o perfil e', abstract)

    def test_xmlarticle_meta_original_language_abstract_without_data_pipe(self):

        fakexylosearticle = Article({'article': {'v40': [{'_': 'pt'}]}, 'title': {}})

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLArticleMetaAbstractsPipe()
        raw, xml = xmlarticle.transform(data)

        abstract = xml.find('./front/article-meta/abstract/p')

        self.assertEqual(None, abstract)

    def test_xmlarticle_meta_translated_abstract_without_data_pipe(self):

        fakexylosearticle = Article({'article': {'v40': [{'_': 'pt'}]}, 'title': {}})

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLArticleMetaAbstractsPipe()
        raw, xml = xmlarticle.transform(data)

        abstract = xml.find('./front/article-meta/trans-abstract/p')

        self.assertEqual(None, abstract)

    def test_xmlarticle_meta_keywords_without_data_pipe(self):

        fakexylosearticle = Article({'article': {'v40': [{'_': 'pt'}]}, 'title': {}})

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLArticleMetaKeywordsPipe()
        raw, xml = xmlarticle.transform(data)

        keywords_language = xml.find('./front/article-meta/kwd-group')

        self.assertEqual(None, keywords_language)

    def test_xmlarticle_meta_keywords_languages_data_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaKeywordsPipe()
        raw, xml = xmlarticle.transform(data)

        keywords_language = sorted([i.get('{http://www.w3.org/XML/1998/namespace}lang') for i in xml.findall('./front/article-meta/kwd-group')])

        self.assertEqual(sorted([u'es', u'pt']), keywords_language)

    def test_xmlarticle_meta_keywords_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaKeywordsPipe()
        raw, xml = xmlarticle.transform(data)

        keywords = sorted([i.text.encode('utf-8') for i in xml.findall('.//kwd')])

        self.assertEqual(sorted([i.encode('utf-8') for i in [
            u'Insuficiencia Renal Crónica',
            u'Terapia de Reemplazo Renal',
            u'Sistemas de Información en Hospital',
            u'Registros de Mortalidad',
            u'Insuficiência Renal Crônica',
            u'Terapia de Substituição Renal',
            u'Sistemas de Informação Hospitalar',
            u'Registros de Mortalidade']]), keywords)

    def test_xml_article_meta_counts_citations_pipe(self):
        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaCountsPipe()
        raw, xml = xmlarticle.transform(data)

        count = xml.find('./front/article-meta/counts/ref-count').get('count')

        self.assertEqual(23, int(count))

    def test_xml_article_meta_counts_pages_pipe(self):
        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaCountsPipe()
        raw, xml = xmlarticle.transform(data)

        count = xml.find('./front/article-meta/counts/page-count').get('count')

        self.assertEqual(11, int(count))

    def test_xml_article_meta_counts_pages_invalid_pages_pipe(self):
        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        self._article_meta.data['article']['v14'][0]['l'] = 'invalidpage'
        self._article_meta.data['article']['v14'][0]['f'] = 'invalidpage'

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaCountsPipe()
        raw, xml = xmlarticle.transform(data)

        count = xml.find('./front/article-meta/counts/page-count').get('count')

        self.assertEqual(0, int(count))

    def test_xml_article_meta_counts_pages_pages_is_none_pipe(self):
        fakexylosearticle = Article({'article': {}})

        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLArticleMetaCountsPipe()
        raw, xml = xmlarticle.transform(data)

        count = xml.find('./front/article-meta/counts/page-count').get('count')

        self.assertEqual(0, int(count))

    def test_xml_article_meta_counts_pages_invalid_pages_first_gt_last_pipe(self):
        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        self._article_meta.data['article']['v14'][0]['l'] = '100'
        self._article_meta.data['article']['v14'][0]['f'] = '110'

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaCountsPipe()
        raw, xml = xmlarticle.transform(data)

        count = xml.find('./front/article-meta/counts/page-count').get('count')

        self.assertEqual(0, int(count))

    def test_xml_article_meta_permission_pipe(self):
        pxml = ET.Element('article')
        pxml.append(ET.Element('front'))

        front = pxml.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaPermissionPipe()
        raw, xml = xmlarticle.transform(data)

        citations = xml.find('./front/articlemeta/permissions/lincense[@license-type="open-access"]')

        self.assertEqual(None, citations)

    def test_xml_citations_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}, 'citatons': {}})

        pxml = ET.Element('article')
        pxml.append(ET.Element('back'))

        back = pxml.find('back')
        back.append(ET.Element('ref-list'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_rsps.XMLArticleMetaKeywordsPipe()
        raw, xml = xmlarticle.transform(data)

        citations = xml.find('./article/back/ref-list/ref')

        self.assertEqual(None, citations)

    def test_xml_citations_count_pipe(self):

        pxml = ET.Element('article')
        pxml.append(ET.Element('back'))

        back = pxml.find('back')
        back.append(ET.Element('ref-list'))

        data = [self._article_meta, pxml]

        xmlarticle = export_rsps.XMLArticleMetaCitationsPipe()
        raw, xml = xmlarticle.transform(data)

        citations = len(xml.findall('./back/ref-list/ref'))

        self.assertEqual(23, citations)


class ExportRSPS_XMLArticleMetaIssueInfoPipe_Tests(unittest.TestCase):

    def setUp(self):
        self._xml = ET.Element('article')
        front = ET.Element('front')
        front.append(ET.Element('article-meta'))
        self._xml.append(front)

    def test_aop(self):
        _raw_json = {
            'issue':
                {'issue':
                    {'v32': [{'_': 'ahead'}]},
                 },
            'article':
                {'v32': [{'_': 'ahead'}]},
            }
        _article = Article(_raw_json)

        data = [_article, self._xml]

        _xml = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = _xml.transform(data)

        self.assertEqual(xml.find('.//article-meta/issue'), None)

    def test_issue(self):
        _raw_json = {
            'issue':
                {'issue':
                    {'v32': [{'_': '4'}]},
                 },
            'article':
                {'v32': [{'_': '4'}]},
            }
        _article = Article(_raw_json)

        data = [_article, self._xml]

        _xml = export_rsps.XMLArticleMetaIssueInfoPipe()
        raw, xml = _xml.transform(data)

        self.assertEqual(xml.findtext('.//article-meta/issue'), '4')
