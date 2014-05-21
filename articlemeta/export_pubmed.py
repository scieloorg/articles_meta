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


class XMLPubDatePipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        if raw.issue == 'ahead':
            pubdate = ET.Element('PubDate', PubStatus='aheadofprint')
        else:
            pubdate = ET.Element('PubDate', PubStatus='ppublish')

        #Year
        if raw.publication_date[0:4]:
            year = ET.Element('Year')
            year.text = raw.publication_date[0:4]
            pubdate.append(year)
        #Month
        if raw.publication_date[5:7]:
            month = ET.Element('Month')
            month.text = raw.publication_date[5:7]
            pubdate.append(month)
        #Day
        if raw.publication_date[8:10]:
            day = ET.Element('Day')
            day.text = raw.publication_date[8:10]
            pubdate.append(day)

        xml.find('./Journal').append(pubdate)

        return data


class XMLReplacesPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        replaces = ET.Element('Replaces')
        replaces.text = raw.publisher_id

        xml.find('./Article').append(replaces)

        return data


class XMLArticleTitlePipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        articletitle = ET.Element('ArticleTitle')
        articletitle.text = raw.original_title()

        xml.find('./Article').append(articletitle)

        return data


class XMLFirstPagePipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        firstpage = ET.Element('FirstPage')
        firstpage.text = raw.start_page

        xml.find('./Article').append(firstpage)

        return data


class XMLLastPagePipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        lastpage = ET.Element('LastPage')
        lastpage.text = raw.end_page

        xml.find('./Article').append(lastpage)

        return data


class XMLElocationIDPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        elocationid = ET.Element('ELocationID', EIdType="pii")
        elocationid.text = raw.publisher_id

        xml.find('./Article').append(elocationid)

        return data


class XMLLanguagePipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        language = ET.Element('Language')
        language.text = raw.original_language()

        xml.find('./Article').append(language)

        return data


class XMLClosePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        data = ET.tostring(xml, encoding="utf-8", method="xml")

        return data
