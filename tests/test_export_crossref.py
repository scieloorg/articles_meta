# coding: utf-8
import unittest
import json
import os
import io

from lxml import etree as ET

from xylose.scielodocument import Article

from articlemeta import export_crossref
from articlemeta import export


class ExportTests(unittest.TestCase):

    def setUp(self):
        self._raw_json = json.loads(
            open(
                os.path.dirname(__file__)+'/fixtures/article_meta.json').read()
            )
        self._article_meta = Article(self._raw_json)

    def test_doi_batch_element(self):

        data = [None, None]

        xmlcrossref = export_crossref.SetupDoiBatchPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual('doi_batch', xml.tag)

    def test_doi_batch_id_element(self):

        xmlcrossref = ET.Element('doi_batch')

        xmlcrossref.append(ET.Element('head'))

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLDoiBatchIDPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual('doi_batch_id', xml.find('head/doi_batch_id').tag)

    def test_depositor_element(self):

        xmlcrossref = ET.Element('doi_batch')

        xmlcrossref.append(ET.Element('head'))

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLDepositorPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><head><depositor><depositor_name>depositor</depositor_name><email_address>name@domain.com</email_address></depositor></head></doi_batch>', ET.tostring(xml))

    def test_registrant_element(self):

        xmlcrossref = ET.Element('doi_batch')

        xmlcrossref.append(ET.Element('head'))

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLRegistrantPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><head><registrant>registrant</registrant></head></doi_batch>', ET.tostring(xml))

    def test_time_stamp_element(self):

        xmlcrossref = ET.Element('doi_batch')

        xmlcrossref.append(ET.Element('head'))

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLTimeStampPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual('timestamp', xml.find('head/timestamp').tag)

    def test_head_element(self):

        xmlcrossref = ET.Element('doi_batch')

        data = [None, xmlcrossref]

        xmlcrossref = export_crossref.XMLHeadPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual('head', xml.find('head').tag)

    def test_body_element(self):

        xmlcrossref = ET.Element('doi_batch')

        data = [None, xmlcrossref]

        xmlcrossref = export_crossref.XMLBodyPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual('body', xml.find('body').tag)

    def test_journal_element(self):

        xmlcrossref = ET.Element('doi_batch')

        xmlcrossref.append(ET.Element('body'))

        data = [None, xmlcrossref]

        xmlcrossref = export_crossref.XMLJournalPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal/></body></doi_batch>', ET.tostring(xml))

    def test_journal_metadata_element(self):

        xmlcrossref = ET.Element('doi_batch')

        body = ET.Element('body')
        body.append(ET.Element('journal'))

        xmlcrossref.append(body)

        data = [None, xmlcrossref]

        xmlcrossref = export_crossref.XMLJournalMetadataPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_metadata/></journal></body></doi_batch>', ET.tostring(xml))

    def test_journal_title_element(self):

        xmlcrossref = ET.Element('doi_batch')

        journal = ET.Element('journal')
        journal.append(ET.Element('journal_metadata'))

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLJournalTitlePipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_metadata><full_title>Revista de Sa&#250;de P&#250;blica</full_title></journal_metadata></journal></body></doi_batch>', ET.tostring(xml))

    def test_abbreviated_journal_title_element(self):

        xmlcrossref = ET.Element('doi_batch')

        journal = ET.Element('journal')
        journal.append(ET.Element('journal_metadata'))

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLAbbreviatedJournalTitlePipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_metadata><abbrev_title>Rev. Sa&#250;de P&#250;blica</abbrev_title></journal_metadata></journal></body></doi_batch>', ET.tostring(xml))

    def test_journal_issn_element(self):

        xmlcrossref = ET.Element('doi_batch')

        journal = ET.Element('journal')
        journal.append(ET.Element('journal_metadata'))

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLISSNPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_metadata><issn media_type="electronic">0034-8910</issn></journal_metadata></journal></body></doi_batch>', ET.tostring(xml))

    def test_journal_issue_element(self):

        xmlcrossref = ET.Element('doi_batch')

        body = ET.Element('body')
        body.append(ET.Element('journal'))

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLJournalIssuePipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_issue/></journal></body></doi_batch>', ET.tostring(xml))

    def test_publication_date_element(self):

        xmlcrossref = ET.Element('doi_batch')

        journal = ET.Element('journal')
        journal.append(ET.Element('journal_issue'))

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLPubDatePipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_issue><publication_date media_type="print"><month>08</month><year>2010</year></publication_date></journal_issue></journal></body></doi_batch>', ET.tostring(xml))

    def test_volume_element(self):

        xmlcrossref = ET.Element('doi_batch')

        journal = ET.Element('journal')
        journal.append(ET.Element('journal_issue'))

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLVolumePipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_issue><journal_volume><volume>44</volume></journal_volume></journal_issue></journal></body></doi_batch>', ET.tostring(xml))

    def test_number_element(self):

        xmlcrossref = ET.Element('doi_batch')

        journal = ET.Element('journal')
        journal.append(ET.Element('journal_issue'))

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLIssuePipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_issue><issue>4</issue></journal_issue></journal></body></doi_batch>', ET.tostring(xml))

    def test_journal_article_element(self):

        xmlcrossref = ET.Element('doi_batch')

        body = ET.Element('body')
        body.append(ET.Element('journal'))

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLJournalArticlePipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_article publication_type="full_text" reference_distribution_opts="any"/></journal></body></doi_batch>', ET.tostring(xml))

    def test_article_titles_element(self):

        xmlcrossref = ET.Element('doi_batch')

        journal_article = ET.Element('journal_article')
        journal_article.set('publication_type', 'full_text')

        journal = ET.Element('journal')
        journal.append(journal_article)

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLArticleTitlesPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_article publication_type="full_text"><titles/></journal_article></journal></body></doi_batch>', ET.tostring(xml))

    def test_article_title_element(self):

        xmlcrossref = ET.Element('doi_batch')

        titles = ET.Element('titles')

        journal_article = ET.Element('journal_article')
        journal_article.set('publication_type', 'full_text')
        journal_article.append(titles)

        journal = ET.Element('journal')
        journal.append(journal_article)

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLArticleTitlePipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_article publication_type="full_text"><titles><title>Perfil epidemiol&#243;gico dos pacientes em terapia renal substitutiva no Brasil, 2000-2004</title></titles></journal_article></journal></body></doi_batch>', ET.tostring(xml))

    def test_article_contributors_element(self):

        xmlcrossref = ET.Element('doi_batch')

        journal_article = ET.Element('journal_article')
        journal_article.set('publication_type', 'full_text')

        journal = ET.Element('journal')
        journal.append(journal_article)

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLArticleContributorsPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_article publication_type="full_text"><contributors><person_name contributor_role="author" sequence="first"><given_name>Mariangela Leal</given_name><surname>Cherchiglia</surname><affiliation>Universidade Federal de Minas Gerais,  BRAZIL</affiliation></person_name><person_name contributor_role="author" sequence="additional"><given_name>Elaine Leandro</given_name><surname>Machado</surname><affiliation>Universidade Federal de Minas Gerais,  BRAZIL</affiliation></person_name><person_name contributor_role="author" sequence="additional"><given_name>Daniele Ara&#250;jo Campo</given_name><surname>Szuster</surname><affiliation>Universidade Federal de Minas Gerais,  BRAZIL</affiliation></person_name><person_name contributor_role="author" sequence="additional"><given_name>Eli Iola Gurgel</given_name><surname>Andrade</surname><affiliation>Universidade Federal de Minas Gerais,  BRAZIL</affiliation></person_name><person_name contributor_role="author" sequence="additional"><given_name>Francisco de Assis</given_name><surname>Ac&#250;rcio</surname><affiliation>Universidade Federal de Minas Gerais,  BRAZIL</affiliation></person_name><person_name contributor_role="author" sequence="additional"><given_name>Waleska Teixeira</given_name><surname>Caiaffa</surname><affiliation>Universidade Federal de Minas Gerais,  BRAZIL</affiliation></person_name><person_name contributor_role="author" sequence="additional"><given_name>Ricardo</given_name><surname>Sesso</surname><affiliation>Universidade Federal de S&#227;o Paulo,  BRAZIL</affiliation></person_name><person_name contributor_role="author" sequence="additional"><given_name>Augusto A</given_name><surname>Guerra Junior</surname><affiliation>Universidade Federal de Minas Gerais,  BRAZIL; Universidade Federal de S&#227;o Paulo,  BRAZIL</affiliation></person_name><person_name contributor_role="author" sequence="additional"><given_name>Odilon Vanni de</given_name><surname>Queiroz</surname><affiliation>Universidade Federal de Minas Gerais,  BRAZIL</affiliation></person_name><person_name contributor_role="author" sequence="additional"><given_name>Isabel Cristina</given_name><surname>Gomes</surname><affiliation>Universidade Federal de Minas Gerais,  BRAZIL</affiliation></person_name></contributors></journal_article></journal></body></doi_batch>', ET.tostring(xml))

    def test_article_publication_date_element(self):

        xmlcrossref = ET.Element('doi_batch')

        journal_article = ET.Element('journal_article')
        journal_article.set('publication_type', 'full_text')

        journal = ET.Element('journal')
        journal.append(journal_article)

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLArticlePubDatePipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_article publication_type="full_text"><publication_date media_type="print"><month>08</month><year>2010</year></publication_date></journal_article></journal></body></doi_batch>', ET.tostring(xml))

    def test_article_pages_element(self):

        xmlcrossref = ET.Element('doi_batch')

        journal_article = ET.Element('journal_article')
        journal_article.set('publication_type', 'full_text')

        journal = ET.Element('journal')
        journal.append(journal_article)

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLPagesPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_article publication_type="full_text"><pages><first_page>639</first_page><last_page>649</last_page></pages></journal_article></journal></body></doi_batch>', ET.tostring(xml))

    def test_article_pid_element(self):

        xmlcrossref = ET.Element('doi_batch')

        journal_article = ET.Element('journal_article')
        journal_article.set('publication_type', 'full_text')

        journal = ET.Element('journal')
        journal.append(journal_article)

        body = ET.Element('body')
        body.append(journal)

        xmlcrossref.append(body)

        data = [self._article_meta, xmlcrossref]

        xmlcrossref = export_crossref.XMLPIDPipe()
        raw, xml = xmlcrossref.transform(data)

        self.assertEqual(b'<doi_batch><body><journal><journal_article publication_type="full_text"><publisher_item><identifier id_type="pii">S0034-89102010000400007</identifier></publisher_item></journal_article></journal></body></doi_batch>', ET.tostring(xml))

    def test_xmlclose_pipe(self):

        pxml = ET.Element('doi_batch')
        pxml.append(ET.Element('head'))

        data = [None, pxml]

        xmlarticle = export_crossref.XMLClosePipe()
        xml = xmlarticle.transform(data)

        self.assertEqual("<?xml version='1.0' encoding='utf-8'?>\n<doi_batch><head/></doi_batch>".encode('utf-8'), xml)

    def test_validating_against_schema(self):

        xml = export.Export(self._raw_json).pipeline_crossref()

        xmlio = ET.parse(io.BytesIO(xml))

        schema_root = ET.parse(open(os.path.dirname(__file__)+'/xsd/scielo_crossref/crossref4.4.0.xsd'))
        schema = ET.XMLSchema(schema_root)

        schema.assertValid(xmlio)

        self.assertTrue(schema.validate(xmlio))
        self.assertEqual(None, schema.assertValid(xmlio))
