import unittest

from pyramid import testing
import pyramid.httpexceptions as exc

from articlemeta import articlemeta


class ViewsTest(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
