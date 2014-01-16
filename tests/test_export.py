# coding: utf-8

import unittest
import xml.etree.ElementTree as ET

from articlemeta import export


class ExportTests(unittest.TestCase):

    def test_setuppipe_element_name(self):

        data = [None, None]

        xmlarticle = export.SetupPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('articles', xml.tag)

    def test_setuppipe_attributes(self):

        data = [None, None]

        xmlarticle = export.SetupPipe()
        raw, xml = xmlarticle.transform(data)

        attributes = ['xmlns:xsi',
                      'xmlns:xlink',
                      'dtd-version',
                      'xsi:noNamespaceSchemaLocation']

        self.assertEqual(attributes, xml.keys())

    def test_xmlarticlepipe(self):

        pxml = ET.Element('articles')

        data = [None, pxml]

        xmlarticle = export.XMLArticlePipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article /></articles>', ET.tostring(xml))

    def test_xmlfrontbackpipe(self):

        pxml = ET.Element('articles')
        pxml.append(ET.Element('article'))

        data = [None, pxml]

        xmlarticle = export.XMLFrontBackPipe()
        raw, xml = xmlarticle.transform(data)

        self.assertEqual('<articles><article><front /><back /></article></articles>', ET.tostring(xml))
