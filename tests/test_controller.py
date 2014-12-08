# coding: utf-8
import os
import unittest
import json
from datetime import datetime
from mocker import Mocker, ANY
from xylose.scielodocument import Article

from articlemeta.controller import (DataBroker,
                                    remove_accents,
                                    gen_citations_title_keys,
                                    gen_title_keys)


class ControllerTest(unittest.TestCase):

    def setUp(self):

        self._raw_json = json.loads(
            open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())
        self._raw_json['_id'] = 'xx'

    def test_gen_title_keys(self):

        title_keys = gen_title_keys(Article(self._raw_json))
        expected = {
            'title_keys': [
                u'perfilepidemiologicodospacientesemterapiarenalsubstitutivanobrasil',
                u'epidemiologicalprofileofpatientsonrenalreplacementtherapyinbrazil',
                u'perfilepidemiologicodelospacientesenterapiarenalsubstitutivaenbrasil',
                u'perfilepidemiologicodospacientesemterapiarenalsubstitutivanobrasilmariangelalealcherchiglia2010',
                u'epidemiologicalprofileofpatientsonrenalreplacementtherapyinbrazilmariangelalealcherchiglia2010',
                u'perfilepidemiologicodelospacientesenterapiarenalsubstitutivaenbrasilmariangelalealcherchiglia2010'
            ]
        }

        self.assertEqual(title_keys, expected)

    def test_gen_title_keys_without_titles(self):

        del(self._raw_json['article']['v12'])

        title_keys = gen_title_keys(Article(self._raw_json))

        self.assertEqual(title_keys, [])

    def test_gen_title_keys_without_authors(self):

        del(self._raw_json['article']['v10'])

        title_keys = gen_title_keys(Article(self._raw_json))

        expected = {
            'title_keys': [
                u'perfilepidemiologicodospacientesemterapiarenalsubstitutivanobrasil',
                u'epidemiologicalprofileofpatientsonrenalreplacementtherapyinbrazil',
                u'perfilepidemiologicodelospacientesenterapiarenalsubstitutivaenbrasil'
            ],
        }

        self.assertEqual(title_keys, expected)

    def test_get_citations_titles(self):

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'preventionofchronickidneydiseaseaglobalchallenge' in citations['citations_keys'])

    def test_get_citations_titles_article_title(self):

        article_citation = {
            "v30": [{u"_": u"Ethn Dis."}],
            "v31": [{u"_": u"16"}],
            "v32": [{u"s": u"2", "_": u"2"}],
            "v12": [{u"l": u"en", u"_": u"End-stage renal disease in sub-Saharan Africa."}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}],
            "v14": [{"_": u"2,5,9"}],
            "v10": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'endstagerenaldiseaseinsubsaharanafrica' in citations['citations_keys'])

    def test_get_citations_without_citations(self):

        self._raw_json['citations'] = []

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertEqual(citations, [])

    def test_get_citations_titles_article_title_with_author_and_year(self):

        article_citation = {
            "v30": [{u"_": u"Ethn Dis."}],
            "v31": [{u"_": u"16"}],
            "v32": [{u"s": u"2", "_": u"2"}],
            "v12": [{u"l": u"en", u"_": u"Aticle title"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}],
            "v14": [{"_": u"2,5,9"}],
            "v10": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'aticletitleelbamgboye2006' in citations['citations_keys'])

    def test_get_citations_titles_thesis_title(self):

        article_citation = {
            "v18": [{u"_": u"Thesis Title"}],
            "v45": [{u"l": u"en", u"_": u"20060000"}],
            "v51": [{"_": u"Thesis Degree"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}],
            "v10": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'thesistitle' in citations['citations_keys'])

    def test_get_citations_titles_thesis_title_with_autor_and_year(self):

        article_citation = {
            "v18": [{u"_": u"Thesis Title"}],
            "v45": [{u"l": u"en", u"_": u"20060000"}],
            "v51": [{"_": u"Thesis Degree"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}],
            "v10": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'thesistitleelbamgboye2006', citations['citations_keys'])

    def test_get_citations_titles_book_title_with_monographic_autor_and_year(self):

        article_citation = {
            "v18": [{u"_": u"Book Title"}],
            "v12": [{u"l": u"en", u"_": u"Chapter Title"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}],
            "v16": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'chaptertitleelbamgboye2006' in citations['citations_keys'])

    def test_get_citations_titles_chapter_title(self):

        article_citation = {
            "v18": [{u"l": u"en", u"_": u"Book Title"}],
            "v12": [{u"l": u"en", u"_": u"Chapter Title"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}],
            "v10": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'chaptertitle' in citations['citations_keys'])

    def test_get_citations_titles_chapter_title_with_author_and_year(self):

        article_citation = {
            "v18": [{u"l": u"en", u"_": u"Book Title"}],
            "v12": [{u"l": u"en", u"_": u"Chapter Title"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}],
            "v10": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'chaptertitleelbamgboye2006', citations['citations_keys'])

    def test_get_citations_titles_conference_title(self):

        article_citation = {
            "v53": [{u"l": u"en", u"_": u"Conference Name"}],
            "v18": [{u"l": u"en", u"_": u"Conference Source"}],
            "v12": [{u"l": u"en", u"_": u"Conference Title"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'conferencetitle' in citations['citations_keys'])

    def test_get_citations_titles_link_title(self):

        article_citation = {
            "v12": [{u"l": u"en", u"_": u"Link Title"}],
            "v37": [{u"_": u"http://www.scielo.br"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'linktitle' in citations['citations_keys'])

    def test_get_citations_titles_link_title_with_author_and_year(self):

        article_citation = {
            "v12": [{u"l": u"en", u"_": u"Link Title"}],
            "v37": [{u"_": u"http://www.scielo.br"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}],
            "v10": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'linktitleelbamgboye2006' in citations['citations_keys'])

    def test_get_citations_titles_link_title_without_date(self):

        article_citation = {
            "v12": [{u"l": u"en", u"_": u"Link Title"}],
            "v37": [{u"_": u"http://www.scielo.br"}],
            "v10": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertEqual(citations['citations_keys'], [u'linktitle', u'linktitle'])

    def test_get_citations_author_year_titles(self):

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertTrue(u'endstagerenaldiseaseinsubsaharanafricaelbamgboye2006' in citations['citations_keys'])

    def test_get_article_available_code(self):

        mocker = Mocker()
        databroker = mocker.mock()
        databroker['articles'].find_one(ANY)
        mocker.result(self._raw_json)
        mocker.replay()

        db = DataBroker(databroker)

        self.assertEqual(db.get_article('xx')['code'], 'S0034-89102010000400007')

    def test_get_article_unavailable_code(self):

        mocker = Mocker()
        databroker = mocker.mock()
        databroker['articles'].find_one(ANY)
        mocker.result(None)
        mocker.replay()

        db = DataBroker(databroker)

        self.assertEqual(db.get_article('xx'), None)

    def test_exists_article_False(self):

        mocker = Mocker()
        databroker = mocker.mock()
        databroker['articles'].find(ANY).count()
        mocker.result(None)
        mocker.replay()

        db = DataBroker(databroker)

        self.assertEqual(db.exists_article('xx'), False)

    def test_check_article_meta(self):

        db = DataBroker(None)

        expected = db._check_article_meta(self._raw_json)

        self.assertEqual(expected['code_issue'], u'0034-891020100004')
        self.assertEqual(expected['code_title'], [u'0034-8910'])
        self.assertEqual(expected['publication_year'], u'2010')
        self.assertEqual(expected['collection'], u'scl')

    def test_check_journal_meta(self):

        db = DataBroker(None)

        expected = db._check_journal_meta(self._raw_json['title'])

        self.assertEqual(expected['code'], [u'0034-8910'])
        self.assertEqual(expected['collection'], u'scl')

    def test_remove_accents(self):

        expected = u'perfilepidemiologicodospacientesemterapiarenalsubstitutivanobrasil'

        self.assertEqual(remove_accents(u'Perfil epidemiológico dos pacientes em terapia renal substitutiva no Brasil, 2000-2004'), expected)

    def test_log_changes_with_valid_params(self):
        mocker = Mocker()
        databroker = mocker.mock()
        document_types = ['article', 'journal']
        events = ['add', 'update', 'delete']

        # db "insert" must be called len(document_types) * len(events) times
        for document_type in document_types:
            for event in events:
                databroker['historychanges_%s' % document_type].insert(ANY)
                mocker.result(123457890)
        mocker.replay()

        db = DataBroker(databroker)

        for document_type in document_types:
            for event in events:
                log_data = {
                    'document_type': document_type,
                    'pid': '123',
                    'collection': 'test_collection',
                    'event': event,
                    'date': datetime.now().isoformat(),
                }
                log_id = db._log_changes(**log_data)
                self.assertEqual(log_id, 123457890)

    def test_historylogs_without_filters(self):
        for document_type in ['article', 'journal']:
            historylogs = json.loads(
                open(os.path.dirname(__file__) +
                     '/fixtures/historylogs_%s.json' % document_type).read()
            )
            mocker = Mocker()
            databroker = mocker.mock()
            databroker['historychanges_%s' % document_type].find(ANY).count()
            mocker.result(historylogs['meta']['total'])
            databroker['historychanges_%s' % document_type].find(ANY).skip(ANY).limit(ANY)
            mocker.result(historylogs['objects'])
            mocker.replay()

            db = DataBroker(databroker)
            result = db.historychanges(document_type)

            self.assertIn('meta', result.keys())
            self.assertEqual(
                historylogs['meta']['total'],
                result['meta']['total']
            )
            self.assertIn('objects', result.keys())
            self.assertEqual(historylogs['objects'], result['objects'])
            self.assertEqual(
                result['objects'][0].keys(),
                ['date', 'pid', 'event', 'collection']
            )
