import unittest
from lxml import etree
from articlemeta.utils import convert_ahref_to_extlink


class TestConvertAtoExtlink(unittest.TestCase):
    def setUp(self):
        self.etree_with_links = etree.fromstring(
            """<xml>
                <a href="">text</a>
                <a href="#local">text</a>
                <a href="https://www.scielo.br">text</a>
            </xml>"""
        )

    def test_should_not_convert_a_to_extlink_when_href_is_empty_or_local(self):
        xml_etree = convert_ahref_to_extlink(self.etree_with_links)
        self.assertEqual(2, len(xml_etree.findall(".//a")))

    def test_should_convert_a_to_extlink_when_href_have_http_string(self):
        xml_etree = convert_ahref_to_extlink(self.etree_with_links)
        self.assertEqual(1, len(xml_etree.findall(".//ext-link")))

