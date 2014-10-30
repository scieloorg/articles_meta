#coding: utf-8
from lxml import etree as ET

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

        xml.find('./Article/Journal').append(publishername)

        return data


class XMLJournalTitlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        journaltitle = ET.Element('JournalTitle')
        journaltitle.text = raw.journal_title

        xml.find('./Article/Journal').append(journaltitle)

        return data


class XMLISSNPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        issn = ET.Element('Issn')
        issn.text = raw.any_issn(priority='print')

        xml.find('./Article/Journal').append(issn)

        return data


class XMLVolumePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        volume = ET.Element('Volume')
        volume.text = raw.volume

        xml.find('./Article/Journal').append(volume)

        return data


class XMLIssuePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        issue = ET.Element('Issue')
        issue.text = raw.issue

        xml.find('./Article/Journal').append(issue)

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

        xml.find('./Article/Journal').append(pubdate)

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


class XMLAuthorListPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        authorlist = ET.Element('AuthorList')

        for authors in raw.authors:
            author = ET.Element('Author')
            authorlist.append(author)

            firstname = ET.Element('FirstName')
            firstname.text = authors['given_names']
            author.append(firstname)

            lastname = ET.Element('LastName')
            lastname.text = authors['surname']
            author.append(lastname)

            if raw.affiliations:
                for aff in raw.affiliations:
                    if aff['index'] == authors['xref'][0]:
                        affiliation = ET.Element('Affiliation')
                        aff_list = []
                        if 'institution' in aff:
                            aff_list.append(aff['institution'])
                        if 'addr_line' in aff:
                            aff_list.append(aff['addr_line'])
                        if 'country' in aff:
                            aff_list.append(aff['country'])
                        affiliation.text = ',  '.join(aff_list)
                        author.append(affiliation)

        xml.find('./Article').append(authorlist)

        return data


class XMLPublicationTypePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        publicationtype = ET.Element('PublicationType')
        publicationtype.text = raw.document_type

        xml.find('./Article').append(publicationtype)

        return data


class XMLArticleIDListPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        articleidlist = ET.Element('ArticleIdList')

        if raw.publisher_id:
            articleidtype = ET.Element('ArticleId', IdType='pii')
            articleidtype.text = raw.publisher_id
            articleidlist.append(articleidtype)

        if raw.doi:
            articleiddoi = ET.Element('ArticleId', IdType='doi')
            articleiddoi.text = raw.doi
            articleidlist.append(articleiddoi)

        xml.find('./Article').append(articleidlist)

        return data


class XMLHistoryPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        history = ET.Element('History')

        #received date
        if raw.receive_date:
            pubdate = ET.Element('PubDate', PubStatus='received')
            #Yeah
            year = ET.Element('Year')
            year.text = raw.receive_date[0:4]
            pubdate.append(year)
            #Month
            month = ET.Element('Month')
            month.text = raw.receive_date[5:7]
            pubdate.append(month)
            #Day
            day = ET.Element('Day')
            day.text = raw.receive_date[8:10]
            pubdate.append(day)
        #acceptance date
        if raw.acceptance_date:
            pubdate = ET.Element('PubDate', PubStatus='accepted')
            #Yeah
            year = ET.Element('Year')
            year.text = raw.acceptance_date[0:4]
            pubdate.append(year)
            #Month
            month = ET.Element('Month')
            month.text = raw.acceptance_date[5:7]
            pubdate.append(month)
            #Day
            day = ET.Element('Day')
            day.text = raw.acceptance_date[8:10]
            pubdate.append(day)
        #ahead of print date
        if raw.ahead_publication_date:
            pubdate = ET.Element('PubDate', PubStatus='aheadofprint')
            #Yeah
            year = ET.Element('Year')
            year.text = raw.ahead_publication_date[0:4]
            pubdate.append(year)
            #Month
            month = ET.Element('Month')
            month.text = raw.ahead_publication_date[5:7]
            pubdate.append(month)
            #Day
            day = ET.Element('Day')
            day.text = raw.ahead_publication_date[8:10]
            pubdate.append(day)

        history.append(pubdate)

        xml.find('./Article').append(history)

        return data


class XMLAbstractPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        abstract = ET.Element('Abstract')
        abstract.text = raw.original_abstract()

        xml.find('./Article').append(abstract)

        return data


class XMLClosePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        data = ET.tostring(xml, method="xml", encoding="utf-8")

        return data
