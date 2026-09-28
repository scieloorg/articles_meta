# coding: utf-8
import json
import os
from unittest import main, TestCase
from unittest.mock import patch

import mongomock

from processing import load_languages
from articlemeta import controller


def mock_static_catalog_init_method(self, collection, fallback_domain=None):
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

    def test_static_catalog_fallback(self):
        """Test that StaticCatalog tries fallback domain when primary fails"""
        
        # Mock do_request to simulate primary domain failure with actual catalog data
        def mock_do_request_primary_fails(url, json=True):
            if 'www.scielo.br' in url:
                return None  # Primary fails
            elif 'antigo.scielo.br' in url:
                # Fallback succeeds with catalog data
                class MockResponse:
                    def iter_lines(self, decode_unicode=None):
                        # Return sample catalog entries
                        return [
                            'serial/rsp/v52/0034-8910-rsp-s1518-87872018052000131.pdf',
                            'serial/rsp/v52/0034-8910-rsp-s1518-87872018052000131.xml',
                        ]
                return MockResponse()
            return None
        
        with patch.object(load_languages, 'do_request', side_effect=mock_do_request_primary_fails):
            # Test with fallback domain - should populate catalog
            catalog = load_languages.StaticCatalog('www.scielo.br', fallback_domain='antigo.scielo.br')
            self.assertIsInstance(catalog.catalog, dict)
            # Verify catalog was populated from fallback
            self.assertIn('rsp', catalog.catalog)
            self.assertIn('v52', catalog.catalog['rsp'])
            
        # Test without fallback domain - should log error and have empty catalog
        def mock_do_request_always_fails(url, json=True):
            return None  # Both primary and fallback fail
        
        with patch.object(load_languages, 'do_request', side_effect=mock_do_request_always_fails):
            with patch.object(load_languages, 'logger') as mock_logger:
                catalog_no_fallback = load_languages.StaticCatalog('www.scielo.br', fallback_domain=None)
                self.assertIsInstance(catalog_no_fallback.catalog, dict)
                # Verify error was logged for each file type (pdf, html, xml)
                error_calls = [call for call in mock_logger.error.call_args_list 
                             if 'Failed to load static catalog' in str(call)]
                self.assertGreaterEqual(len(error_calls), 3)  # At least one for each file type

    @patch.object(
        load_languages.StaticCatalog, "__init__", mock_static_catalog_init_method
    )
    def test_run_with_fallback_domain(self):
        """Test run function with fallback_domain parameter"""
        mocked_articlemeta_db = mongomock.MongoClient().db
        mocked_articlemeta_db['collections'].insert_many([
            {
                "acron": "scl",
                "code": "scl",
                "domain": "www.scielo.br"
            },
        ])
        mocked_articlemeta_db['articles'].insert_one(self._raw_json)

        # Test with fallback_domain parameter
        load_languages.run(['scl'],
                           mocked_articlemeta_db,
                           all_records=True,
                           forced_url='www.scielo.br',
                           fallback_domain='antigo.scielo.br')

        document = mocked_articlemeta_db['articles'].find_one(
            {'code': self._raw_json['code']},
            {'_id': 0, 'citations': 0}
        )
        self.assertIsNotNone(document)


if __name__ == '__main__':
    main()
