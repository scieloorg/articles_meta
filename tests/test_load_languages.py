# coding: utf-8
import json
import os
from unittest import main, TestCase
from unittest.mock import patch

import mongomock

from processing import load_languages
from articlemeta import controller


def mock_static_catalog_init_method(self, collection):
    self.catalog = {
        "rsp": {
            "v52": {
                'html': [],
                'pdf': [
                    '0034-8910-rsp-s1518-87872018052000131-pt',
                    '0034-8910-rsp-s1518-87872018052000131',
                    'pt_0034-8910-rsp-s1518-87872018052000131'
                ],
                'xml': [
                    '0034-8910-rsp-s1518-87872018052000131'
                ]
            }
        }
    }

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

    def test_get_acron_issueid_fname_without_extension(self):
        get_file_id = load_languages.get_acron_issueid_fname_without_extension
        self.assertEqual(
            get_file_id('delta/v32n2/1678-460X-delta-32-02-00543.xml'),
            ['delta', 'v32n2', '1678-460x-delta-32-02-00543']
        )
        self.assertEqual(
            get_file_id('V:\\Scielo\\serial\\dpjo\\v15n3\\markup\\05.html'),
            ['dpjo', 'v15n3', '05']
        )
        self.assertEqual(
            get_file_id('C:\\SciELO\\Serial\\aa\\v34n1\\markup\\v34n1a06.html'),
            ['aa', 'v34n1', 'v34n1a06']
        )
        self.assertEqual(
            get_file_id(
                'd:/c.917173/scielo/serial.lilacs//'
                'mioc/v51/markup/v51/tomo51(f1)_17-74.pdf'),
            ['mioc', 'v51', 'tomo51(f1)_17-74']
        )
        self.assertEqual(
            get_file_id(
                '/scielo/serial.lilacs//mioc/v82s3/'
                'markup/v82s3/vol82(fsup3)_II.pdf'),
            ['mioc', 'v82s3', 'vol82(fsup3)_ii']
        )

    @patch.object(
        load_languages.StaticCatalog, "__init__", mock_static_catalog_init_method
    )
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
