# coding: utf-8

import unittest
from pyramid import testing
from articlemeta.decorators import LogHistoryChange



class LogHistoryChangeDecoratorTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_invoke_without_params_must_crash(self):
        with self.assertRaises(TypeError):
            @LogHistoryChange()
            class A:
                pass

    def test_invoke_with_params_must_not_crash(self):
        try:
            @LogHistoryChange(document_type='SOMETHING', event_type='ANYTHING')
            class A:
                pass
        except Exception as e:
            self.fail("LogHistoryChange decorator raised %s unexpectedly!" % s)
