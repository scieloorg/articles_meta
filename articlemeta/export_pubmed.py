#coding: utf-8
import xml.etree.ElementTree as ET

import plumber


class SetupArticleSetPipe(plumber.Pipe):

    def transform(self, data):

        xml = ET.Element('ArticleSet')

        return data, xml


class XMLArticlePipe(plumber.Pipe):

    def tranform(self, data):
        raw, xml = data

        article = ET.Element('Article')

        xml.append(article)

        return data


class XMLJournalPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        journal = ET.Element('Journal')
        journal.text = raw.journal_title

        xml.find('./Article').append(journal)

        return data


class XMLClosePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        data = ET.tostring(xml, encoding="utf-8", method="xml")

        return data
