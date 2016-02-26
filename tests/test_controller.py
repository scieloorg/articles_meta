# coding: utf-8
import os
import unittest
import json
from datetime import datetime
from mocker import Mocker, ANY
from xylose.scielodocument import Article

from articlemeta.controller import DataBroker


class ControllerTest(unittest.TestCase):

    def setUp(self):

        self._raw_json = json.loads(
            open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())
        self._raw_json['_id'] = 'xx'

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
                    'code': '123',
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
            databroker['historychanges_%s' % document_type].find(ANY).skip(ANY).limit(ANY).sort("date")
            mocker.result(historylogs['objects'])
            mocker.replay()

            db = DataBroker(databroker)
            result = db.historychanges(document_type)

            # assert date filters are correct in meta
            self.assertIn('meta', result.keys())
            self.assertIn('filter', result['meta'].keys())
            self.assertIn('date', result['meta']['filter'].keys())
            self.assertEqual(['$lte', '$gt'], result['meta']['filter']['date'].keys())

            self.assertEqual(
                historylogs['meta']['total'],
                result['meta']['total']
            )
            self.assertIn('objects', result.keys())
            self.assertEqual(historylogs['objects'], result['objects'])
            self.assertEqual(
                result['objects'][0].keys(),
                ['date', 'code', 'event', 'collection']
            )
