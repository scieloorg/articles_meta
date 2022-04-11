import unittest
import json
from datetime import datetime

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
    def test_pdfs_paths_only_one_doi(self):
        with open("./tests/fixtures/article_meta_pdfs_paths_only_one_doi.json") as fp:
            data = json.loads(fp.read())
        expected = {
            "code": "S0004-27492000000500002",
            "collection": "scl",
            "processing_date": "2007-04-03T00:00:00.000Z",
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
        self.assertEqual(expected, controller._pdfs_paths(data))

    def test_pdfs_paths_aop(self):
        with open("./tests/fixtures/article_meta_pdfs_paths_aop.json") as fp:
            data = json.loads(fp.read())
        expected = {
            "code": "S0004-27492000000500002",
            "collection": "scl",
            "processing_date": "2007-04-03T00:00:00.000Z",
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
        self.assertEqual(expected, controller._pdfs_paths(data))

