# coding: utf-8
import unittest
from articlemeta.export import CustomArticle as Article


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.article_json = {
            "article": {
                "v40": [{"_": "pt"}],
                "v601": [{"_": "es"}, {"_": "en"}],
                "v237": [{"_": "10.1590/S0034-89102010000400007"}],
                },
            "body": {
                "es": "Body ES",
                "en": "Body EN"
            },
        }

    def test_derivate_translations_doi(self):
        article = Article(self.article_json)
        self.assertEqual(
            article.derivate_translations_doi,
            {
                "es": "10.1590/S0034-89102010000400007.es",
                "en": "10.1590/S0034-89102010000400007.en",
            },
        )

    def test_document_doi_and_lang_no_doi(self):
        article_json = {
            "article": {
                "v40": [{"_": "pt"}],
                "v601": [{"_": "es"}, {"_": "en"}],
                },
            }
        article_json.update({"doi_for_translation": "derivate"})
        article = Article(article_json)
        self.assertEqual(article.document_doi_and_lang, [])

    def test_document_doi_and_lang_only_one_doi(self):
        article_json = {
            "article": {
                "v40": [{"_": "pt"}],
                "v601": [{"_": "es"}, {"_": "en"}],
                "v237": [{"_": "10.1590/S0034-89102010000400007"}],
            }
        }
        article = Article(article_json)
        self.assertEqual(
            article.document_doi_and_lang, [("pt", "10.1590/S0034-89102010000400007")]
        )

    def test_document_doi_and_lang_derivated_doi(self):
        article_json = {
            "article": {
                "v40": [{"_": "pt"}],
                "v601": [{"_": "es"}, {"_": "en"}],
                "v237": [{"_": "10.1590/S0034-89102010000400007"}],
            }
        }
        article_json.update({"doi_for_translation": "derivate"})
        article = Article(article_json)
        self.assertEqual(
            article.document_doi_and_lang,
            [
                ("pt", "10.1590/S0034-89102010000400007"),
                ("es", "10.1590/S0034-89102010000400007.es"),
                ("en", "10.1590/S0034-89102010000400007.en"),
            ],
        )

    def test_document_doi_and_lang_provided_doi(self):
        article_json = {
            "article": {
                "v40": [{"_": "pt"}],
                "v601": [{"_": "es"}, {"_": "en"}],
                "v237": [{"_": "10.1590/S0034-89102010000400007"}],
                "v337": [
                    {"d": "10.1590/S0034-89102010000400007", "l": "pt"},
                    {"d": "10.1590/S0034-89102010000400007.spanish", "l": "es"},
                    {"d": "10.1590/S0034-89102010000400007.english", "l": "en"},
                ],
            }
        }
        article = Article(article_json)
        self.assertEqual(
            article.document_doi_and_lang,
            [
                ("pt", "10.1590/S0034-89102010000400007"),
                ("es", "10.1590/S0034-89102010000400007.spanish"),
                ("en", "10.1590/S0034-89102010000400007.english"),
            ],
        )

    def test_document_doi_and_lang_provided_doi_with_configuration_derivated(self):
        article_json = {
            "article": {
                "v40": [{"_": "pt"}],
                "v601": [{"_": "es"}, {"_": "en"}],
                "v237": [{"_": "10.1590/S0034-89102010000400007"}],
                "v337": [
                    {"d": "10.1590/S0034-89102010000400007", "l": "pt"},
                    {"d": "10.1590/S0034-89102010000400007.spanish", "l": "es"},
                    {"d": "10.1590/S0034-89102010000400007.english", "l": "en"},
                ],
            }
        }
        article_json.update({"doi_for_translation": "derivate"})
        article = Article(article_json)
        self.assertEqual(
            article.document_doi_and_lang,
            [
                ("pt", "10.1590/S0034-89102010000400007"),
                ("es", "10.1590/S0034-89102010000400007.spanish"),
                ("en", "10.1590/S0034-89102010000400007.english"),
            ],
        )

    def test_document_doi_and_lang_provided_and_derivated_doi(self):
        article_json = {
            "article": {
                "v40": [{"_": "pt"}],
                "v601": [{"_": "es"}, {"_": "en"}],
                "v237": [{"_": "10.1590/S0034-89102010000400007"}],
                "v337": [
                    {"d": "10.1590/S0034-89102010000400007", "l": "pt"},
                    {"d": "10.1590/S0034-89102010000400007.english", "l": "en"},
                ],
            }
        }
        article_json.update({"doi_for_translation": "derivate"})
        article = Article(article_json)
        self.assertEqual(
            article.document_doi_and_lang,
            [
                ("pt", "10.1590/S0034-89102010000400007"),
                ("es", "10.1590/S0034-89102010000400007.es"),
                ("en", "10.1590/S0034-89102010000400007.english"),
            ],
        )
