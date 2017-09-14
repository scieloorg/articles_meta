import unittest
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

