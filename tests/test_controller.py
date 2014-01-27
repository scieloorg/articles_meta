# encoding: utf-8
import os
import unittest
import json

from mocker import Mocker, ANY

from articlemeta.controller import DataBroker, remove_accents


class ControllerTest(unittest.TestCase):

    def setUp(self):

        self._raw_json = json.loads(
            open(os.path.dirname(__file__)+'/fixtures/article_meta.json').read())
        self._raw_json['_id'] = 'xx'

    def test_get_article_available_code(self):

        mocker = Mocker()
        databroker = mocker.mock()
        databroker['articles'].find_one(ANY)
        mocker.result(self._raw_json)
        mocker.replay()

        db = DataBroker(databroker)

        self.assertEqual(db.get_article('xx')['code'], 'S0034-89102010000400007')

    def test_get_article_unavailable_code(self):

        mocker = Mocker()
        databroker = mocker.mock()
        databroker['articles'].find_one(ANY)
        mocker.result(None)
        mocker.replay()

        db = DataBroker(databroker)

        self.assertEqual(db.get_article('xx'), None)

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

    def test_remove_accents(self):

        expected = u'perfilepidemiologicodospacientesemterapiarenalsubstitutivanobrasil'

        self.assertEqual(remove_accents(u'Perfil epidemiológico dos pacientes em terapia renal substitutiva no Brasil, 2000-2004'), expected)














