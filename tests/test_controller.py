# coding: utf-8
import os
import unittest
import json

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
            'no_accents_strings': [
                u'perfilepidemiologicodospacientesemterapiarenalsubstitutivanobrasil',
                u'epidemiologicalprofileofpatientsonrenalreplacementtherapyinbrazil',
                u'perfilepidemiologicodelospacientesenterapiarenalsubstitutivaenbrasil'
            ],
            'no_accents_strings_author_year': [
                u'perfilepidemiologicodospacientesemterapiarenalsubstitutivanobrasilmariangelalealcherchiglia2010',
                u'epidemiologicalprofileofpatientsonrenalreplacementtherapyinbrazilmariangelalealcherchiglia2010',
                u'perfilepidemiologicodelospacientesenterapiarenalsubstitutivaenbrasilmariangelalealcherchiglia2010'
            ]
        }

        self.assertEqual(title_keys, expected)

    def test_gen_title_keys_without_titles(self):

        del(self._raw_json['article']['v12'])

        title_keys = gen_title_keys(Article(self._raw_json))

        self.assertEqual(title_keys, None)

    def test_gen_title_keys_without_authors(self):

        del(self._raw_json['article']['v10'])

        title_keys = gen_title_keys(Article(self._raw_json))

        expected = {
            'no_accents_strings': [
                u'perfilepidemiologicodospacientesemterapiarenalsubstitutivanobrasil',
                u'epidemiologicalprofileofpatientsonrenalreplacementtherapyinbrazil',
                u'perfilepidemiologicodelospacientesenterapiarenalsubstitutivaenbrasil'
            ],
            'no_accents_strings_author_year': []
        }

        self.assertEqual(title_keys, expected)

    def test_get_citations_titles(self):

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertEqual(citations['citations_title_no_accents'][0],
                         u'endstagerenaldiseaseinsubsaharanafrica')

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

        self.assertEqual(citations['citations_title_no_accents'][0],
                         u'endstagerenaldiseaseinsubsaharanafrica')

    def test_get_citations_without_citations(self):

        self._raw_json['citations'] = []

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertEqual(citations, None)

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

        self.assertEqual(citations['citations_title_author_year_no_accents'][0],
                         u'aticletitleelbamgboye2006')

    def test_get_citations_titles_thesis_title(self):

        article_citation = {
            "v18": [{u"_": u"Thesis Title"}],
            "v45": [{u"l": u"en", u"_": u"Thesis Title"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}],
            "v10": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertEqual(citations['citations_title_no_accents'][0],
                         u'thesistitle')

    def test_get_citations_titles_thesis_title_with_autor_and_year(self):

        article_citation = {
            "v18": [{u"_": u"Thesis Title"}],
            "v45": [{u"l": u"en", u"_": u"Thesis Title"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}],
            "v10": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertEqual(citations['citations_title_author_year_no_accents'][0],
                         u'thesistitleelbamgboye2006')

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

        self.assertEqual(citations['citations_title_author_year_no_accents'][0],
                         u'chaptertitleelbamgboye2006')

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

        self.assertEqual(citations['citations_title_no_accents'][0],
                         u'chaptertitle')

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

        self.assertEqual(citations['citations_title_author_year_no_accents'][0],
                         u'chaptertitleelbamgboye2006')

    def test_get_citations_titles_conference_title(self):

        article_citation = {
            "v53": [{u"l": u"en", u"_": u"Conference Title"}],
            "v65": [{"_": u"20060000"}],
            "v64": [{"_": u"2006"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertEqual(citations['citations_title_no_accents'][0],
                         u'conferencetitle')

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

        self.assertEqual(citations['citations_title_no_accents'][0],
                         u'linktitle')

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

        self.assertEqual(citations['citations_title_author_year_no_accents'][0],
                         u'linktitleelbamgboye2006')

    def test_get_citations_titles_link_title_without_date(self):

        article_citation = {
            "v12": [{u"l": u"en", u"_": u"Link Title"}],
            "v37": [{u"_": u"http://www.scielo.br"}],
            "v10": [{"s": u"Bamgboye", "r": u"ND", "_": u"", "n": u"EL"}]
            }

        self._raw_json['citations'] = [article_citation]

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertEqual(citations['citations_title_author_year_no_accents'], None)

    def test_get_citations_author_year_titles(self):

        article = Article(self._raw_json)

        citations = gen_citations_title_keys(article)

        self.assertEqual(citations['citations_title_author_year_no_accents'][0],
                         u'endstagerenaldiseaseinsubsaharanafricaelbamgboye2006')

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














