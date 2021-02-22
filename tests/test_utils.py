import unittest
from lxml import etree
from articlemeta.utils import convert_ahref_to_extlink
from processing import escape_html_http_tags


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


class TestProcessingEscapeHTTPTags(unittest.TestCase):

    def test_should_escape_http_tags(self):
        string = "<http://www.scielo.br>Texto"
        expected = "&lt;http://www.scielo.br&gt;Texto"
        self.assertEqual(expected, escape_html_http_tags(string))

    def test_should_escape_all_html_tags_in_the_string(self):
        string = "<http://www.scielo.br>Texto<p><https://www.scielo.org></p>"
        expected = "&lt;http://www.scielo.br&gt;Texto<p>&lt;https://www.scielo.org&gt;</p>"
        self.assertEqual(expected, escape_html_http_tags(string))

    def test_should_not_scape_regular_tags_or_texts(self):
        string = "<p>Some text available in &lt;http://www.scielo.br&gt;</p>"
        expected = "<p>Some text available in &lt;http://www.scielo.br&gt;</p>"
        self.assertEqual(expected, escape_html_http_tags(string))
