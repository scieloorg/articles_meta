import unittest
import json
from datetime import datetime

import mongomock

from articlemeta import controller

class FunctionDatesToStringTests(unittest.TestCase):
    def test_converts_datatime_in_processing_date_value(self):
        data = {'processing_date': datetime(2017, 9, 14)}
        expected_result = {'processing_date': '2017-09-14'}
        self.assertEqual(controller.dates_to_string(data), expected_result)

    def test_converts_datatime_in_processing_date_values_dict(self):
        data = {'processing_date': {
            '$lte': datetime(2017, 9, 15), '$gte': datetime(2017, 9, 14)}}
        expected_result = {'processing_date': {
            '$lte': '2017-09-15', '$gte': '2017-09-14'}}
        self.assertEqual(controller.dates_to_string(data), expected_result)

    def test_converts_datatime_in_date_value(self):
        data = {'date': datetime(2017, 9, 14)}
        expected_result = {'date': '2017-09-14'}
        self.assertEqual(controller.dates_to_string(data), expected_result)

    def test_converts_datatime_in_date_values_dict(self):
        data = {'date': {
            '$lte': datetime(2017, 9, 15), '$gte': datetime(2017, 9, 14)}}
        expected_result = {'date': {
            '$lte': '2017-09-15', '$gte': '2017-09-14'}}
        self.assertEqual(controller.dates_to_string(data), expected_result)

    def test_converts_datatime_in_created_at_value(self):
        data = {'created_at': datetime(2017, 9, 14)}
        expected_result = {'created_at': '2017-09-14'}
        self.assertEqual(controller.dates_to_string(data), expected_result)

    def test_converts_datatime_in_updated_at_value(self):
        data = {'updated_at': datetime(2017, 9, 14)}
        expected_result = {'updated_at': '2017-09-14'}
        self.assertEqual(controller.dates_to_string(data), expected_result)

    def test_arbitrary_types_are_preserved(self):
        data = {'foo': 'bar', 'zaz': 5, 'bla': [1, 2, 3]}
        expected_result = {'foo': 'bar', 'zaz': 5, 'bla': [1, 2, 3]}
        self.assertEqual(controller.dates_to_string(data), expected_result)

    def test_input_data_is_not_mutated(self):
        data = {'processing_date': datetime(2017, 9, 14)}
        data_copy = data.copy()
        _ = controller.dates_to_string(data)
        self.assertEqual(data, data_copy)


class PdfsPathsTests(unittest.TestCase):
    def test_counter_dict_only_one_doi(self):
        with open("./tests/fixtures/article_meta_counter_dict_only_one_doi.json") as fp:
            data = json.loads(fp.read())
        expected = {
            "created_at": "2007-04-03T00:00:00.000Z",
            "updated_at": "2007-04-04T00:00:00.000Z",
            "processing_date": "2007-04-03T00:00:00.000Z",
            "publication_date": "2007-04",
            "publication_year": "2007",
            "collection": "scl",
            "code": "S0004-27492000000500002",
            "code_title": ["0004-2749", "1234-0987"],
            "journal_acronym": "aa",
            "text_langs": ["fr", "de"],
            "default_language": "pt",
            "pdfs": [{
                "lang": "pt",
                "path": "pdf/aa/v34n1/v34n1a13.pdf",
                "doi": "10.1590/S0044-59672004000100013",
                "checked": False,
            },
            {
                "lang": "en",
                "path": "pdf/aa/v34n1/en_v34n1a13.pdf",
                "doi": "10.1590/S0044-59672004000100013",
                "checked": False,
            }
        ]}
        result = controller._counter_dict(data)
        self.assertDictEqual(expected, result)

    def test_counter_dict_aop(self):
        with open("./tests/fixtures/article_meta_counter_dict_aop.json") as fp:
            data = json.loads(fp.read())
        expected = {
            "created_at": "2007-04-03T00:00:00.000Z",
            "updated_at": "2007-04-04T00:00:00.000Z",
            "processing_date": "2007-04-03T00:00:00.000Z",
            "publication_date": "2007-04",
            "publication_year": "2007",
            "collection": "scl",
            "code": "S0004-27492000000500002",
            "code_title": ["0004-2749", "1234-0987"],
            "journal_acronym": "aa",
            "text_langs": ["fr", "de"],
            "default_language": "pt",
            "previous_pid": "S0044-59672004005000013",
            "pdfs": [{
                    "lang": "pt",
                    "path": "pdf/aa/2017nahead/v34n1a13.pdf",
                    "doi": "10.1590/S0044-59672004000100013",
                    "checked": False,
                },
                {
                    "lang": "en",
                    "path": "pdf/aa/2017nahead/en_v34n1a13.pdf",
                    "doi": "10.1590/S0044-59672004000100013",
                    "checked": False,
                }]
        }
        result = controller._counter_dict(data)
        self.assertDictEqual(expected, result)

    def test_counter_dict_one_doi_for_each(self):
        with open("./tests/fixtures/article_meta_counter_dict_one_doi_for_each.json") as fp:
            data = json.loads(fp.read())
        expected = {
            "created_at": "2007-04-03T00:00:00.000Z",
            "updated_at": "2007-04-04T00:00:00.000Z",
            "processing_date": "2007-04-03T00:00:00.000Z",
            "publication_date": "2007-04",
            "publication_year": "2007",
            "collection": "scl",
            "code": "S0004-27492000000500002",
            "code_title": ["0004-2749", "1234-0987"],
            "journal_acronym": "aa",
            "text_langs": ["fr", "de"],
            "default_language": "pt",
            "pid_v3": "GlaPaaeoKaeKaPjaeHaHjae",
            "pdfs": [{
                "lang": "pt",
                "path": "pdf/aa/v34n1/v34n1a13.pdf",
                "doi": "10.1590/S0044-59672004000100013.pt",
                "checked": False,
            },
            {
                "lang": "en",
                "path": "pdf/aa/v34n1/en_v34n1a13.pdf",
                "doi": "10.1590/S0044-59672004000100013.en",
                "checked": False,
            }
        ]}
        result = controller._counter_dict(data)
        self.assertDictEqual(expected, result)


class CrossmarkPolicyDoiTests(unittest.TestCase):
    def setUp(self):
        self.db = mongomock.MongoClient().db
        self.db.crossmark_policies.insert_one({
            'issns': ['2237-9622', '1679-4974'],
            'doi_url': '10.1590/scielo.crossmark.policy',
            'content_url': 'https://www.scielo.br/crossmark/policy',
        })
        self.broker = controller.DataBroker(self.db)

    def test_both_issns_return_the_same_doi(self):
        expected = '10.1590/scielo.crossmark.policy'
        self.assertEqual(
            expected, self.broker.get_crossmark_policy_doi(['2237-9622']))
        self.assertEqual(
            expected, self.broker.get_crossmark_policy_doi(['1679-4974']))

    def test_several_issns_are_queried_at_once(self):
        expected = '10.1590/scielo.crossmark.policy'
        self.assertEqual(
            expected,
            self.broker.get_crossmark_policy_doi(
                ['0000-0000', '1679-4974']),
        )

    def test_missing_issn_returns_none(self):
        self.assertIsNone(self.broker.get_crossmark_policy_doi(['0000-0000']))

    def test_dx_doi_url_prefix_is_stripped(self):
        self.db.crossmark_policies.insert_one({
            'issns': ['0034-8910'],
            'doi_url': '10.1590/rsp.crossmark.policy',
            'content_url': 'https://www.scielo.br/crossmark/rsp',
        })
        self.assertEqual(
            '10.1590/rsp.crossmark.policy',
            self.broker.get_crossmark_policy_doi(['0034-8910']))
