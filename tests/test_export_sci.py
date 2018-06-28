# coding: utf-8
import unittest
from lxml import etree as ET
import json
import os

from lxml import etree
from xylose.scielodocument import Article

from articlemeta import export_sci
from articlemeta import export


class XMLCitationTests(unittest.TestCase):

    def setUp(self):

        self._raw_json = json.loads(open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())
        self._citation_meta = Article(self._raw_json).citations[0]

        self._xmlcitation = export_sci.XMLCitation()

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

        publicationtype = xml.find('./element-citation[@publication-type="article"]').get('publication-type')

        self.assertEqual(u'article', publicationtype)

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

    def test_xml_citation_url_pipe(self):

        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [{'v37': [{'_': 'http://www.scielo.br'}]}]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.URIPipe().transform(data)

        expected = xml.find('./element-citation/ext-link').text

        self.assertEqual(u'http://www.scielo.br', expected)

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

        result = xml.find('./element-citation/person-group/name/given-names').text

        self.assertEqual('EL', result)

    def test_xml_citation_person_group_surname_pipe(self):

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [self._citation_meta, pxml]

        raw, xml = self._xmlcitation.PersonGroupPipe().transform(data)

        result = xml.find('./element-citation/person-group/name/surname').text

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

    def test_xml_citation_conference_pipe(self):
        conf_name = {
            '_': u'Workshop Internacional sobre Clima'
                 u' e Recursos Naturais nos Países de Língua Portuguesa',
            'n': 'II'
        }
        conf_location = {
            '_': u'Bragança',
        }
        citation = {
            'v53': [conf_name],
            'v56': [conf_location],
        }
        fakexylosearticle = Article({'article': {},
                                     'title': {},
                                     'citations': [citation]}).citations[0]

        pxml = ET.Element('ref')
        pxml.append(ET.Element('element-citation'))

        data = [fakexylosearticle, pxml]

        raw, xml = self._xmlcitation.ConferencePipe().transform(data)

        self.assertEqual(
            conf_name['_'], xml.find('./element-citation/conf-name').text)
        self.assertEqual(
            conf_location['_'], xml.find('./element-citation/conf-loc').text)


class ExportTests(unittest.TestCase):

    def setUp(self):
        self._raw_json = json.loads(open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())
        self._article_meta = Article(self._raw_json)

    def test_xmlclose_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        data = [None, pxml]

        xmlarticle = export_sci.XMLClosePipe()
        xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article/></articles>'.encode('utf-8'), xml)

    def test_setuppipe_element_name(self):

        data = [None, None]

        xmlarticle = export_sci.SetupArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('articles', xml.tag)

    def test_setuppipe_attributes(self):

        data = [None, None]

        xmlarticle = export_sci.SetupArticlePipe()
        raw, xml = xmlarticle.transform(data)

        attributes = sorted(['dtd-version', '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'])

        self.assertEqual(attributes, sorted(xml.keys()))

    def test_xmlarticle_pipe(self):

        pxml = ET.Element('articles')

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article lang_id="pt" article-type="research-article"/></articles>'.encode('utf-8'), ET.tostring(xml))

    def test_xmlfront_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        data = [None, pxml]

        xmlarticle = export_sci.XMLFrontPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article><front><journal-meta/><article-meta/></front></article></articles>'.encode('utf-8'), ET.tostring(xml))

    def test_xmljournal_id_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLJournalMetaJournalIdPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article><front><journal-meta><journal-id journal-id-type="publisher">rsp</journal-id></journal-meta></front></article></articles>'.encode('utf-8'), ET.tostring(xml))

    def test_xmljournal_meta_journal_title_group_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLJournalMetaJournalTitleGroupPipe()
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

        xmlarticle = export_sci.XMLJournalMetaISSNPipe()
        raw, xml = xmlarticle.transform(data)

        issn = xml.find('./article/front/journal-meta/issn').text

        self.assertEqual(u'0034-8910', issn)

    def test_xmljournal_meta_collection_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLJournalMetaCollectionPipe()
        raw, xml = xmlarticle.transform(data)

        collection = xml.find('./article/front/journal-meta/collection').text

        self.assertEqual(u'SciELO Brazil', collection)

    def test_xmljournal_meta_publisher_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('journal-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLJournalMetaPublisherPipe()
        raw, xml = xmlarticle.transform(data)

        publishername = xml.find('./article/front/journal-meta/publisher/publisher-name').text

        self.assertEqual(u'Faculdade de Saúde Pública da Universidade de São Paulo', publishername)

    def test_xml_article_meta_unique_article_id_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaUniqueArticleIdPipe()
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

        xmlarticle = export_sci.XMLArticleMetaArticleIdPublisherPipe()
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

        xmlarticle = export_sci.XMLArticleMetaArticleIdDOIPipe()
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

        xmlarticle = export_sci.XMLArticleMetaArticleIdDOIPipe()

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

        xmlarticle = export_sci.XMLArticleMetaArticleCategoriesPipe()
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

        xmlarticle = export_sci.XMLArticleMetaArticleCategoriesPipe()
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

        xmlarticle = export_sci.XMLArticleMetaTitleGroupPipe()
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

        xmlarticle = export_sci.XMLArticleMetaTranslatedTitleGroupPipe()
        raw, xml = xmlarticle.transform(data)

        titles = sorted([i.find('trans-title').text.encode('utf-8') for i in xml.findall('./article/front/article-meta/title-group/trans-title-group')])

        self.assertEqual(sorted([
            'Epidemiological profile of patients on renal replacement therapy in Brazil, 2000-2004'.encode('utf-8'),
            'Perfil epidemiológico de los pacientes en terapia renal substitutiva en Brasil, 2000-2004'.encode('utf-8')
        ]), titles)

    def test_xmlarticle_meta_translated_title_group_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        articlemeta = front.find('article-meta')
        articlemeta.append(ET.Element('title-group'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_sci.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        titles = [i.find('trans-title').text for i in xml.findall('./article/front/article-meta/title-group/trans-title-group')]

        self.assertEqual([], titles)

    def test_xmlarticle_meta_contrib_group_author_names_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        fullnames = [' '.join([i.find('given-names').text, i.find('surname').text]) for i in xml.findall('./article/front/article-meta/contrib-group/contrib/name')]

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

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        fullnames = [i.text for i in xml.findall('./article/front/article-meta/contrib-group/contrib/role')]

        self.assertEqual([u'ND', u'ND', u'ND', u'ND', u'ND', u'ND', u'ND',
                          u'ND', u'ND', u'ND'], fullnames)

    def test_xmlarticle_meta_contrib_group_author_xrefs_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        fullnames = [i.get('rid') for i in xml.findall('./article/front/article-meta/contrib-group/contrib/xref')]

        self.assertEqual([u'A01', u'A01', u'A01', u'A01', u'A01', u'A01', u'A02',
                          u'A01', u'A02', u'A01', u'A03'], fullnames)

    def test_xmlarticle_meta_contrib_group_author_without_xrefs_pipe(self):

        del(self._raw_json['article']['v71'])
        article_meta = Article(self._raw_json)

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        fullnames = [i.get('rid') for i in xml.findall('./article/front/article-meta/contrib-group/contrib/xref')]

        self.assertEqual([u'A01', u'A01', u'A01', u'A01', u'A01', u'A01', u'A02',
                          u'A01', u'A02', u'A01', u'A03'], fullnames)

    def test_xmlarticle_meta_contrib_group_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_sci.XMLArticleMetaContribGroupPipe()
        raw, xml = xmlarticle.transform(data)

        titles = [i.find('contrib-group').text for i in xml.findall('./article/front/article-meta/contrib-group/contrib')]

        self.assertEqual([], titles)

    def test_xmlarticle_meta_affiliation_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}})

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_sci.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        affiliations = [i.find('institution').text for i in xml.findall('./article/front/article-meta/aff')]

        self.assertEqual([], affiliations)

    def test_xmlarticle_meta_affiliation_institution_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        affiliations = [i.find('institution').text for i in xml.findall('./article/front/article-meta/aff')]

        self.assertEqual(sorted([u'Universidade Federal de Minas Gerais',
                          u'Universidade Federal de São Paulo',
                          u'Universidade Federal de Minas Gerais']), sorted(affiliations))

    def test_xmlarticle_meta_affiliation_index_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        indexes = [i.get('id') for i in xml.findall('./article/front/article-meta/aff')]

        self.assertEqual(sorted([u'A01',
                          u'A02',
                          u'A03']), sorted(indexes))

    def test_xmlarticle_meta_affiliation_country_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaAffiliationPipe()
        raw, xml = xmlarticle.transform(data)

        countries = [i.find('country').text for i in xml.findall('./article/front/article-meta/aff')]

        self.assertEqual([u'BRAZIL',
                          u'BRAZIL',
                          u'BRAZIL'], countries)

    def test_xmlarticle_meta_general_info_pub_year_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaDatesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        pub_year = xml.find('./article/front/article-meta/pub-date/year').text

        self.assertEqual(u'2010', pub_year)

    def test_xmlarticle_meta_general_info_pub_month_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaDatesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        pub_month = xml.find('./article/front/article-meta/pub-date/month').text

        self.assertEqual(u'08', pub_month)

    def test_xmlarticle_meta_general_info_first_page_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaPagesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        fpage = xml.find('./article/front/article-meta/fpage').text

        self.assertEqual(u'639', fpage)

    def test_xmlarticle_meta_general_info_without_first_page_pipe(self):

        del(self._article_meta.data['article']['v14'][0]['f'])

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaPagesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        fpage = xml.find('./article/front/article-meta/fpage')

        self.assertEqual(None, fpage)

    def test_xmlarticle_meta_general_info_last_page_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaPagesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        lpage = xml.find('./article/front/article-meta/lpage').text

        self.assertEqual(u'649', lpage)

    def test_xmlarticle_meta_general_info_without_last_page_pipe(self):

        del(self._article_meta.data['article']['v14'][0]['l'])

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaPagesInfoPipe()
        raw, xml = xmlarticle.transform(data)

        lpage = xml.find('./article/front/article-meta/lpage')

        self.assertEqual(None, lpage)

    def test_xmlarticle_meta_general_info_volume_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        volume = xml.find('./article/front/article-meta/volume').text

        self.assertEqual(u'44', volume)

    def test_xmlarticle_meta_general_info_without_volume_pipe(self):

        del(self._article_meta.data['issue']['issue']['v31'])

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        volume = xml.find('./article/front/article-meta/volume').text

        self.assertEqual('0', volume)

    def test_xmlarticle_meta_general_info_issue_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./article/front/article-meta/issue').text

        self.assertEqual(u'4', issue)

    def test_xmlarticle_meta_general_info_without_issue_pipe(self):

        del(self._article_meta.data['issue']['issue']['v32'])

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./article/front/article-meta/issue').text

        self.assertEqual('0', issue)

    def test_xmlarticle_meta_general_info_elocation_pipe(self):

        self._article_meta.data['article']['v14'][0]['e'] = 'eloc1'

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaElocationInfoPipe()
        raw, xml = xmlarticle.transform(data)

        eloc = xml.find('./article/front/article-meta/elocation-id').text

        self.assertEqual(u'eloc1', eloc)

    def test_xmlarticle_meta_general_info_without_elocation_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaElocationInfoPipe()
        raw, xml = xmlarticle.transform(data)

        eloc = xml.find('./article/front/article-meta/elocation-id')

        self.assertEqual(None, eloc)

    def test_xmlarticle_meta_general_info_suppl_vol_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        del(self._article_meta.data['issue']['issue']['v32'])
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '1'}]

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./article/front/article-meta/issue').text

        self.assertEqual(u'suppl 1', issue)

    def test_xmlarticle_meta_general_info_suppl_vol_0_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        del(self._article_meta.data['issue']['issue']['v32'])
        self._article_meta.data['issue']['issue']['v31'] = [{'_': '10'}]
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '0'}]

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./article/front/article-meta/issue').text

        self.assertEqual(u'suppl', issue)

    def test_xmlarticle_meta_general_info_suppl_issue_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        self._article_meta.data['issue']['issue']['v31'] = [{'_': '10'}]
        self._article_meta.data['issue']['issue']['v32'] = [{'_': '1'}]
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '2'}]

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./article/front/article-meta/issue').text

        self.assertEqual(u'1 suppl 2', issue)

    def test_xmlarticle_meta_general_info_suppl__vol_0_issue_1_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        self._article_meta.data['issue']['issue']['v31'] = [{'_': '10'}]
        self._article_meta.data['issue']['issue']['v32'] = [{'_': '1'}]
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '0'}]

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./article/front/article-meta/issue').text

        self.assertEqual(u'1 suppl', issue)

    def test_xmlarticle_meta_general_info_suppl__vol_10_issue_20_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        self._article_meta.data['issue']['issue']['v31'] = [{'_': '10'}]
        self._article_meta.data['issue']['issue']['v32'] = [{'_': '20'}]
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '0'}]

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./article/front/article-meta/issue').text

        self.assertEqual(u'20 suppl', issue)

    def test_xmlarticle_meta_general_info_suppl__vol_10_issue_20_suppl_10_pipe(self):

        self._article_meta.data['issue']['issue']['v65'] = [{'_': '201008'}]
        self._article_meta.data['issue']['issue']['v31'] = [{'_': '10'}]
        self._article_meta.data['issue']['issue']['v32'] = [{'_': '20'}]
        self._article_meta.data['issue']['issue']['v131'] = [{'_': '10'}]

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaIssueInfoPipe()
        raw, xml = xmlarticle.transform(data)

        issue = xml.find('./article/front/article-meta/issue').text

        self.assertEqual(u'20 suppl 10', issue)

    def test_xmlarticle_meta_general_info_fulltext_uri_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaURLsPipe()
        raw, xml = xmlarticle.transform(data)

        uri = xml.find('./article/front/article-meta/self-uri[@content-type="full_text_page"]').get('href')

        self.assertEqual(u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0034-89102010000400007&lng=en&tlng=en', uri)

    def test_xmlarticle_meta_general_info_issue_uri_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaURLsPipe()
        raw, xml = xmlarticle.transform(data)

        uri = xml.find('./article/front/article-meta/self-uri[@content-type="issue_page"]').get('href')

        self.assertEqual(u'http://www.scielo.br/scielo.php?script=sci_issuetoc&pid=0034-891020100004&lng=en', uri)

    def test_xmlarticle_meta_general_info_journal_uri_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaURLsPipe()
        raw, xml = xmlarticle.transform(data)

        uri = xml.find('./article/front/article-meta/self-uri[@content-type="journal_page"]').get('href')

        self.assertEqual(u'http://www.scielo.br/scielo.php?script=sci_serial&pid=0034-8910&lng=en', uri)

    def test_xmlarticle_meta_original_language_abstract_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaAbstractsPipe()
        raw, xml = xmlarticle.transform(data)

        abstract = xml.find('./article/front/article-meta/abstract/p').text[0:30]

        self.assertEqual(u'OBJETIVO: Descrever o perfil e', abstract)

    def test_xmlarticle_meta_original_language_abstract_without_data_pipe(self):

        fakexylosearticle = Article({'article': {'v40': [{'_': 'pt'}]}, 'title': {}})

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_sci.XMLArticleMetaAbstractsPipe()
        raw, xml = xmlarticle.transform(data)

        abstract = xml.find('./article/front/article-meta/abstract/p')

        self.assertEqual(None, abstract)

    def test_xmlarticle_meta_translated_abstract_without_data_pipe(self):

        fakexylosearticle = Article({'article': {'v40': [{'_': 'pt'}]}, 'title': {}})

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_sci.XMLArticleMetaAbstractsPipe()
        raw, xml = xmlarticle.transform(data)

        abstract = xml.find('./article/front/article-meta/trans-abstract/p')

        self.assertEqual(None, abstract)

    def test_xmlarticle_meta_keywords_without_data_pipe(self):

        fakexylosearticle = Article({'article': {'v40': [{'_': 'pt'}]}, 'title': {}})

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_sci.XMLArticleMetaKeywordsPipe()
        raw, xml = xmlarticle.transform(data)

        keywords_language = xml.find('./article/front/article-meta/kwd-group')

        self.assertEqual(None, keywords_language)

    def test_xmlarticle_meta_keywords_languages_data_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaKeywordsPipe()
        raw, xml = xmlarticle.transform(data)

        keywords_language = sorted([i.get('lang_id').encode('utf-8') for i in xml.findall('./article/front/article-meta/kwd-group')])

        self.assertEqual(
            sorted(['en'.encode('utf-8'), 'es'.encode('utf-8'), 'pt'.encode('utf-8')]), keywords_language)

    def test_xmlarticle_meta_keywords_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('article-meta'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaKeywordsPipe()
        raw, xml = xmlarticle.transform(data)

        keywords = sorted([i.text.encode('utf-8') for i in xml.findall('.//kwd')])

        self.assertEqual(sorted([
            'Renal Insufficiency, Chronic'.encode('utf-8'),
            'Renal Replacement Therapy'.encode('utf-8'),
            'Hospital Information Systems'.encode('utf-8'),
            'Mortality Registries'.encode('utf-8'),
            'Insuficiencia Renal Crónica'.encode('utf-8'),
            'Terapia de Reemplazo Renal'.encode('utf-8'),
            'Sistemas de Información en Hospital'.encode('utf-8'),
            'Registros de Mortalidad'.encode('utf-8'),
            'Insuficiência Renal Crônica'.encode('utf-8'),
            'Terapia de Substituição Renal'.encode('utf-8'),
            'Sistemas de Informação Hospitalar'.encode('utf-8'),
            'Registros de Mortalidade'.encode('utf-8')]), keywords)

    def test_xml_citations_without_data_pipe(self):

        fakexylosearticle = Article({'article': {}, 'title': {}, 'citatons': {}})

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('back'))

        back = article.find('back')
        back.append(ET.Element('ref-list'))

        data = [fakexylosearticle, pxml]

        xmlarticle = export_sci.XMLArticleMetaKeywordsPipe()
        raw, xml = xmlarticle.transform(data)

        citations = xml.find('./articles/article/back/ref-list/ref')

        self.assertEqual(None, citations)

    def test_xml_citations_count_pipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        article = pxml.find('article')
        article.append(ET.Element('back'))

        back = article.find('back')
        back.append(ET.Element('ref-list'))

        data = [self._article_meta, pxml]

        xmlarticle = export_sci.XMLArticleMetaCitationsPipe()
        raw, xml = xmlarticle.transform(data)

        citations = len(xml.findall('./article/back/ref-list/ref'))

        self.assertEqual(23, citations)

    @unittest.skip("demonstrating skipping")
    def test_validating_against_schema(self):

        xml = export.Export(self._raw_json).pipeline_sci()

        xsd = open('tests/xsd/scielo_sci/ThomsonReuters_publishing.xsd', 'rb').read()
        schema_root = etree.XML(xsd)

        schema = etree.XMLSchema(schema_root)
        xmlparser = etree.XMLParser(schema=schema)

        expected = etree.fromstring(xml, xmlparser).tag

        self.assertEqual('articles', expected)
