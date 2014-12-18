import unittest

from pyramid import testing
from mocker import Mocker, ANY
import pyramid.httpexceptions as exc
from articlemeta.controller import DataBroker, get_dbconn


class IndexesTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_ensure_indexes_of_historychanges(self):
        for document_type in ['article', 'journal']:
            # with
            expected_index_key = [(u'date', 1), (u'collection', 1), (u'pid', 1)]
            expected_index = {
                'date_1_collection_1_pid_1': {
                    'key': expected_index_key,
                }
            }
            # mock databroker.<collection>.index_information()
            mocker = Mocker()
            databroker = mocker.mock()
            databroker['historychanges_%s' % document_type].index_information()
            mocker.result(expected_index)
            mocker.replay()

            dbroker = DataBroker(databroker)
            # when
            index_info = dbroker.db['historychanges_%s' % document_type].index_information()
            history_index_info_key = index_info['date_1_collection_1_pid_1']['key']
            # then
            self.assertEqual(expected_index_key, history_index_info_key)
