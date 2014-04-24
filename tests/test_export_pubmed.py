#coding: utf-8
import unittest
import xml.etree.ElementTree as ET
import json
import os

from lxml import etree
from xylose.scielodocument import Article

from articlemeta import export_pubmed
from articlemeta import export


class ExportTests(unittest.TestCase):

    def setUp(self):
