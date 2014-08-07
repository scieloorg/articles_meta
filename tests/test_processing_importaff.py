# coding: utf-8

import unittest
from processing import importaffiliation


class ProcessingImportAffiliationTests(unittest.TestCase):

    def setUp(self):
        class MockArticle(object):
            def __init__(self):
                self.publisher_id = u'S0001-37652013000100001'
                self.affiliations = [
                    {
                        'index': u'aff1',
                        'addr_line': u'Rio de Janeiro',
                        'institution': u'Museu Nacional/UFRJ',
                        'country': u'Brasil'
                    }
                ]

        self.mockarticle = MockArticle()

    def test_parse_csv_line_ok_isis_mfn(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['mfn'], u'27136')

    def test_parse_csv_line_ok_pid(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'
        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['pid'], u'S0001-37652013000100001')

    def test_parse_csv_line_ok_publication_year(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['publication_year'], u'2013')

    def test_parse_csv_line_ok_journal_title(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['journal_title'], u'An. Acad. Bras. Ciênc.')

    def test_parse_csv_line_ok_issue_label(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'
        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['issue_label'], u'v85n1')

    def test_parse_csv_line_ok_aff_index(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['affiliation_index'], u'aff1')

    def test_parse_csv_line_ok_makup_aff_name(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'
        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['markup_affiliation_name'], u'Museu Nacional/UFRJ')

    def test_parse_csv_line_ok_makup_aff_country(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'
        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['markup_affiliation_country'], u'Brasil')

    def test_parse_csv_line_ok_normalizes_aff_name(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['normalized_affiliation_name'], u'Universidade Federal do Rio de Janeiro')

    def test_parse_csv_line_ok_normalized_aff_country(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['normalized_affiliation_country'], u'Brazil')

    def test_parse_csv_line_ok_normalized_aff_country(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['normalized_affiliation_iso_3661_country'], u'BR')

    def test_parse_csv_line_ok_collection(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertEqual(result['collection'], u'scl')

    def test_parse_csv_line_invalid_pid(self):

        line = u'27136|S000137652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertFalse(result)

    def test_parse_csv_line_invalid_size_more(self):

        line = u'|27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertFalse(result)

    def test_parse_csv_line_invalid_size_less(self):

        line = u'27136S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        result = importaffiliation.parse_csv_line(line.split('|'))

        self.assertFalse(result)

    def test_is_valid_pid_true(self):
        pid = u'S0001-37652013000100001'

        result = importaffiliation.is_valid_pid(pid)

        self.assertTrue(result, pid)

    def test_is_valid_pid_false(self):
        pid = u'S000137652013000100001'

        result = importaffiliation.is_valid_pid(pid)

        self.assertFalse(result, pid)

    def test_is_clean_checked_true(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        parsed_line = importaffiliation.parse_csv_line(line.split('|'))

        self.assertTrue(
            importaffiliation.is_clean_checked(parsed_line, self.mockarticle)
        )

    def test_is_clean_checked_false_different_pid(self):

        line = u'27136|S0001-37652013000100002|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        parsed_line = importaffiliation.parse_csv_line(line.split('|'))

        self.assertFalse(
            importaffiliation.is_clean_checked(parsed_line, self.mockarticle)
        )

    def test_is_clean_checked_false_not_match_aff(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|af1|Museu Nacional/UFJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        parsed_line = importaffiliation.parse_csv_line(line.split('|'))

        self.assertFalse(
            importaffiliation.is_clean_checked(parsed_line, self.mockarticle)
        )

    def test_is_clean_checked_false_record_without_affiliations(self):

        line = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        parsed_line = importaffiliation.parse_csv_line(line.split('|'))

        self.mockarticle.affiliations = None

        self.assertFalse(
            importaffiliation.is_clean_checked(parsed_line, self.mockarticle)
        )

    def test_is_like_json(self):

        line1 = u'27136|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff1|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'
        line2 = u'27137|S0001-37652013000100001|scl|2013|An. Acad. Bras. Ciênc.|v85n1|aff2|Museu Nacional/UFRJ|Brasil|Universidade Federal do Rio de Janeiro|Brazil|BR'

        data = [
            importaffiliation.parse_csv_line(line1.split('|')),
            importaffiliation.parse_csv_line(line2.split('|'))
        ]

        result = importaffiliation.isis_like_json(data)

        expected = [
            {
                'i': "AFF1",
                'p': "BR",
                '_': "Universidade Federal do Rio de Janeiro"
            },
            {
                'i': "AFF2",
                'p': "BR",
                '_': "Universidade Federal do Rio de Janeiro"
            },
        ]

        self.assertEqual(result[0]['i'], expected[0]['i'])
        self.assertEqual(result[0]['p'], expected[0]['p'])
        self.assertEqual(result[0]['_'], expected[0]['_'])
        self.assertEqual(result[1]['i'], expected[1]['i'])
        self.assertEqual(result[1]['p'], expected[1]['p'])
        self.assertEqual(result[1]['_'], expected[1]['_'])
