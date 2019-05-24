import unittest
from unittest.mock import patch, MagicMock
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


class DataBrokerTests(unittest.TestCase):
    def setUp(self):
        self.mk_db_suffixes = MagicMock()
        self.mk_db_suffixes.find_one.return_value = None
        self.mk_db_client = {
            'journals': [],
            'issues': [],
            'articles': [],
            'name_suffixes': self.mk_db_suffixes,
        }

    def test_DataBroker_is_name_suffix_not_found(self):
        databroker = controller.DataBroker(self.mk_db_client)
        name_suffix = databroker.is_name_suffix(suffix="jr")
        self.mk_db_suffixes.find_one.assert_called_once_with({"suffix": "jr"})
        self.assertFalse(name_suffix)

    def test_DataBroker_is_name_suffix_lower_case_suffix(self):
        databroker = controller.DataBroker(self.mk_db_client)
        name_suffix = databroker.is_name_suffix(suffix="JR")
        self.mk_db_suffixes.find_one.assert_called_once_with({"suffix": "jr"})

    def test_DataBroker_is_name_suffix_without_period(self):
        databroker = controller.DataBroker(self.mk_db_client)
        name_suffix = databroker.is_name_suffix(suffix="Jr.")
        self.mk_db_suffixes.find_one.assert_called_once_with({"suffix": "jr"})

    def test_DataBroker_is_name_suffix_accepts_alphanumeric(self):
        databroker = controller.DataBroker(self.mk_db_client)
        name_suffix = databroker.is_name_suffix(suffix="3rd")
        self.mk_db_suffixes.find_one.assert_called_once_with({"suffix": "3rd"})

    def test_DataBroker_is_name_suffix(self):
        self.mk_db_suffixes.find_one.return_value = {"suffix": "jr"}
        self.mk_db_client['name_suffixes'] = self.mk_db_suffixes
        databroker = controller.DataBroker(self.mk_db_client)
        name_suffix = databroker.is_name_suffix(suffix="jr")
        self.assertTrue(name_suffix)

    def test_DataBroker_add_name_suffix_checks_if_suffix_exists(self):
        self.mk_db_suffixes.find.return_value.count.return_value = 1
        databroker = controller.DataBroker(self.mk_db_client)
        databroker.add_name_suffix({"suffix": "jr"})
        self.mk_db_suffixes.find.assert_called_once_with({"suffix": "jr"})

    def test_DataBroker_add_name_suffix_does_not_add_it_if_suffix_exists(self):
        self.mk_db_suffixes.find.return_value.count.return_value = 1
        databroker = controller.DataBroker(self.mk_db_client)
        databroker.add_name_suffix({"suffix": "jr"})
        self.mk_db_suffixes.update_one.assert_not_called()

    def test_DataBroker_add_name_suffix_adds_it_if_suffix_does_not_exist(self):
        self.mk_db_suffixes.find.return_value.count.return_value = 0
        databroker = controller.DataBroker(self.mk_db_client)
        databroker.add_name_suffix({"suffix": "jr"})
        self.mk_db_suffixes.update_one.assert_called_once_with(
            {"suffix": "jr"},
            {'$set': {"suffix": "jr"}},
            upsert=True
        )
