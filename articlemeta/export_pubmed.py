#coding: utf-8
import xml.etree.ElementTree as ET

import plumber


class SetupArticleSetPipe(plumber.Pipe):

    def transform(self, data):

        xml = ET.Element('ArticleSet')

        return data, xml


class XMLArticlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        article = ET.Element('Article')

        xml.append(article)

        return data


class XMLJournalPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        journal = ET.Element('Journal')

        xml.find('./Article').append(journal)

        return data


class XMLPublisherNamePipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        publishername = ET.Element('PublisherName')
        publishername.text = raw.publisher_name

        xml.find('./Journal').append(publishername)

        return data


class XMLJournalTitlePipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        journaltitle = ET.Element('JournalTitle')
        journaltitle.text = raw.journal_title

        xml.find('./Journal').append(journaltitle)

        return data


class XMLISSNPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        issn = ET.Element('Issn')
        issn.text = raw.any_issn(priority='print')

        xml.find('./Journal').append(issn)

        return data


class XMLVolumePipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        volume = ET.Element('Volume')
        volume.text = raw.volume

        xml.find('./Journal').append(volume)

        return data


class XMLIssuePipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        issue = ET.Element('Issue')
        issue.text = raw.issue

        xml.find('./Journal').append(issue)

        return data


class XMLArticleTitlePipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        articletitle = ET.Element('ArticleTitle')
        articletitle.text = raw.original_title()

        xml.find('./Article').append(articletitle)

        return data


class XMLClosePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        data = ET.tostring(xml, encoding="utf-8", method="xml")

        return data
