# coding: utf-8
import json
import os
from unittest import main, TestCase
from unittest.mock import patch

import mongomock

from processing import load_languages
from articlemeta import controller


class LoadLanguageTest(TestCase):

    def setUp(self):
        class MockedDB:
            def __init__(self):
                self.db = {
                    'collections': [
                        {
                            "acron": "scl",
                            "code": "scl",
                            "domain": "www.scielo.br"
                        },
                        {
                            "acron": "spa",
                            "code": "spa",
                            "domain": "www.scielosp.org"
                        },
                    ]
                }
        article_meta = os.path.dirname(__file__) + \
            '/fixtures/article_meta_spa.json'
        with open(article_meta) as data:
            self._raw_json = json.loads(data.read())

        self.mocked_db = MockedDB()

    def test_run(self):
        mocked_articlemeta_db = mongomock.MongoClient().db
        mocked_articlemeta_db['collections'].insert_many([
            {
                "acron": "scl",
                "code": "scl",
                "domain": "www.scielo.br"
            },
            {
                "acron": "spa",
                "code": "spa",
                "domain": "www.scielosp.org"
            },
        ])
        mocked_articlemeta_db['articles'].insert_one(self._raw_json)

        load_languages.run(['spa'],
                           mocked_articlemeta_db,
                           all_records=True,
                           forced_url='www.scielo.br')

        document = mocked_articlemeta_db['articles'].find_one(
            {'code': self._raw_json['code']},
            {'_id': 0, 'citations': 0}
        )
        self.assertIsNotNone(document)
        self.assertIsNotNone(document.get('fulltexts'))
        self.assertEqual(self._raw_json['fulltexts']['html'],
                         document['fulltexts']['html'])
        self.assertIsNotNone(document['fulltexts'].get('pdf'))


if __name__ == '__main__':
    main()
