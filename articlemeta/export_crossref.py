# coding: utf-8
from lxml import etree as ET
import re
import os
import uuid

from datetime import datetime

import plumber

SUPPLBEG_REGEX = re.compile(r'^0 ')
SUPPLEND_REGEX = re.compile(r' 0$')


class SetupDoiBatchPipe(plumber.Pipe):

    def transform(self, data):

        nsmap = {
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'jats': 'http://www.ncbi.nlm.nih.gov/JATS1',
            'xml': 'http://www.w3.org/XML/1998/namespace'
        }

        el = ET.Element('doi_batch', nsmap=nsmap)
        el.set('version', '4.4.0')
        el.set('xmlns', 'http://www.crossref.org/schema/4.4.0')
        el.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', 'http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd')

        return data, el


class XMLHeadPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('head')

        xml.append(el)

        return data


class XMLBodyPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('body')

        xml.append(el)

        return data


class XMLDoiBatchIDPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('doi_batch_id')

        el.text = uuid.uuid4().hex

        xml.find('./head').append(el)

        return data


class XMLTimeStampPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('timestamp')

        el.text = datetime.now().strftime('%Y%m%d%H%M%S')

        xml.find('./head').append(el)

        return data


class XMLDepositorPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('depositor')

        depositor_name = ET.Element('depositor_name')
        depositor_name.text = os.environ.get('DEPOSITOR_NAME', 'depositor')
        email_address = ET.Element('email_address')
        email_address.text = os.environ.get('DEPOSITOR_EMAIL_ADRRESS', 'name@domain.com')

        el.append(depositor_name)
        el.append(email_address)

        xml.find('./head').append(el)

        return data


class XMLRegistrantPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('registrant')

        el.text = os.environ.get('CROSSREF_REGISTRANT', 'registrant')

        xml.find('./head').append(el)

        return data


class XMLJournalPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('journal')

        xml.find('./body').append(el)

        return data


class XMLJournalMetadataPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('journal_metadata')

        xml.find('./body/journal').append(el)

        return data


class XMLJournalTitlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('full_title')
        el.text = raw.journal.title

        xml.find('./body/journal/journal_metadata').append(el)

        return data


class XMLAbbreviatedJournalTitlePipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.journal.abbreviated_title:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        el = ET.Element('abbrev_title')
        el.text = raw.journal.abbreviated_title

        xml.find('./body/journal/journal_metadata').append(el)

        return data


class XMLISSNPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.journal.print_issn:
            el = ET.Element('issn')
            el.text = raw.journal.print_issn
            el.set('media_type', 'print')
            xml.find('./body/journal/journal_metadata').append(el)

        if raw.journal.electronic_issn:
            el = ET.Element('issn')
            el.text = raw.journal.electronic_issn
            el.set('media_type', 'electronic')
            xml.find('./body/journal/journal_metadata').append(el)

        return data


class XMLJournalIssuePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('journal_issue')

        xml.find('./body/journal').append(el)

        return data


class XMLPubDatePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        if raw.issue == 'ahead':
            el = ET.Element('publication_date', media_type='aheadofprint')
        else:
            el = ET.Element('publication_date', media_type='print')

        # Day
        if raw.publication_date[8:10]:
            day = ET.Element('day')
            day.text = raw.publication_date[8:10]
            el.append(day)
        # Month
        if raw.publication_date[5:7]:
            month = ET.Element('month')
            month.text = raw.publication_date[5:7]
            el.append(month)
        # Year
        if raw.publication_date[0:4]:
            year = ET.Element('year')
            year.text = raw.publication_date[0:4]
            el.append(year)

        xml.find('./body/journal/journal_issue').append(el)

        return data


class XMLVolumePipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.issue.volume:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        volume = ET.Element('volume')
        volume.text = raw.issue.volume

        el = ET.Element('journal_volume')
        el.append(volume)

        xml.find('./body/journal/journal_issue').append(el)

        return data


class XMLIssuePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        label_volume = raw.issue.volume.replace('ahead', '0') if raw.issue.volume else '0'
        label_issue = raw.issue.number.replace('ahead', '0') if raw.issue.number else '0'

        label_suppl_issue = ' suppl %s' % raw.issue.supplement_number if raw.issue.supplement_number else ''

        if label_suppl_issue:
            label_issue += label_suppl_issue

        label_suppl_volume = ' suppl %s' % raw.issue.supplement_volume if raw.issue.supplement_volume else ''

        if label_suppl_volume:
            label_issue += label_suppl_volume

        label_issue = SUPPLBEG_REGEX.sub('', label_issue)
        label_issue = SUPPLEND_REGEX.sub('', label_issue)

        if label_issue.strip():
            el = ET.Element('issue')
            el.text = label_issue
            xml.find('./body/journal/journal_issue').append(el)

        return data


class XMLJournalArticlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('journal_article')
        el.set('publication_type', 'full_text')

        xml.find('./body/journal').append(el)

        return data


class XMLArticleTitlesPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('titles')

        xml.find('./body/journal/journal_article').append(el)

        return data


class XMLArticleTitlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('title')
        el.text = raw.original_title() or '[NO TITLE AVAILABLE]'

        xml.find('./body/journal/journal_article/titles').append(el)

        return data


class XMLArticleContributorsPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('contributors')

        for ndx, authors in enumerate(raw.authors):
            author = ET.Element('person_name')
            author.set('contributor_role', 'author')

            seq = 'first' if ndx == 0 else 'additional'
            author.set('sequence', seq)
            el.append(author)

            firstname = ET.Element('given_name')
            firstname.text = authors['given_names']
            author.append(firstname)

            lastname = ET.Element('surname')
            lastname.text = authors['surname']
            author.append(lastname)

        if raw.affiliations:
            for ndx, aff in enumerate(raw.affiliations):
                affiliation = ET.Element('organization')
                seq = 'first' if ndx == 0 else 'additional'
                affiliation.set('contributor_role', 'author')
                affiliation.set('sequence', seq)
                aff_list = []
                if 'institution' in aff:
                    aff_list.append(aff['institution'])
                if 'addr_line' in aff:
                    aff_list.append(aff['addr_line'])
                if 'country' in aff:
                    aff_list.append(aff['country'])

                affiliation.text = ',  '.join(aff_list)
                el.append(affiliation)

        xml.find('./body/journal/journal_article').append(el)

        return data


class XMLArticleAbstractPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.original_abstract() or not raw.translated_abstracts():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        if raw.original_abstract():
            paragraph = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}p')
            paragraph.text = raw.original_abstract()
            el = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}abstract')
            el.set('{http://www.w3.org/XML/1998/namespace}lang', raw.original_language())
            el.append(paragraph)
            xml.find('./body/journal/journal_article').append(el)

        for language, body in raw.translated_abstracts().items():
            paragraph = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}p')
            paragraph.text = body
            el = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}abstract')
            el.set('{http://www.w3.org/XML/1998/namespace}lang', language)
            el.append(paragraph)
            xml.find('./body/journal/journal_article').append(el)

        return data


class XMLArticlePubDatePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('publication_date')
        el.set('media_type', "print")

        # Day
        if raw.publication_date[8:10]:
            day = ET.Element('day')
            day.text = raw.publication_date[8:10]
            el.append(day)
        # Month
        if raw.publication_date[5:7]:
            month = ET.Element('month')
            month.text = raw.publication_date[5:7]
            el.append(month)
        # Year
        if raw.publication_date[0:4]:
            year = ET.Element('year')
            year.text = raw.publication_date[0:4]
            el.append(year)

        xml.find('./body/journal/journal_article').append(el)

        return data


class XMLPagesPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.start_page:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        el = ET.Element('pages')

        if raw.start_page:
            firstpage = ET.Element('first_page')
            firstpage.text = raw.start_page
            el.append(firstpage)

        if raw.end_page:
            lastpage = ET.Element('last_page')
            lastpage.text = raw.end_page
            el.append(lastpage)

        if raw.elocation:
            otherpage = ET.Element('other_pages')
            otherpage.text = raw.end_page
            el.append(otherpage)

        xml.find('./body/journal/journal_article').append(el)

        return data


class XMLPIDPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        identifier = ET.Element('identifier')
        identifier.set('id_type',  'pii')
        identifier.text = raw.publisher_id

        el = ET.Element('publisher_item')
        el.append(identifier)

        xml.find('./body/journal/journal_article').append(el)

        return data


class XMLDOIDataPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.doi:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        doi = ET.Element('doi')
        doi.text = raw.doi

        resource = ET.Element('resource')
        resource.text = raw.html_url(language=raw.original_language())

        el = ET.Element('doi_data')
        el.append(doi)
        el.append(resource)

        xml.find('./body/journal/journal_article').append(el)

        return data


class XMLArticleCitationsPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.citations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        article = xml.find('./body/journal/journal_article')
        article.append(ET.Element('citation_list'))

        citations = article.find('citation_list')

        cit = XMLCitation()
        for citation in raw.citations:
            citations.append(cit.deploy(citation)[1])

        return data


class XMLCitation(object):

    def __init__(self):
        self._ppl = plumber.Pipeline(self.SetupCitationPipe(),
                                     self.CitationIdPipe(),
                                     self.ISSNPipe(),
                                     self.JournalTitlePipe(),
                                     self.ThesisTitlePipe(),
                                     self.AuthorPipe(),
                                     self.VolumePipe(),
                                     self.IssuePipe(),
                                     self.StartPagePipe(),
                                     self.DatePipe(),
                                     self.ArticleTitlePipe(),
                                     self.ISBNPipe(),
                                     self.SeriesTitlePipe(),
                                     self.VolumeTitlePipe(),
                                     self.EditionPipe())

    class SetupCitationPipe(plumber.Pipe):

        def transform(self, data):

            xml = ET.Element('citation')

            return data, xml

    class CitationIdPipe(plumber.Pipe):
        def transform(self, data):
            raw, xml = data

            ref = xml.find('.')

            ref.set('key', 'ref{0}'.format(str(raw.index_number)))

            return data

    class ArticleTitlePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.article_title:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            articletitle = ET.Element('article_title')

            articletitle.text = raw.article_title

            xml.find('.').append(articletitle)

            return data

    class SeriesTitlePipe(plumber.Pipe):

        def precond(data):
            raw, xml = data

            if not raw.source or not raw.publication_type == 'book':
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            booktitle = ET.Element('series_title')

            booktitle.text = raw.source

            xml.find('.').append(booktitle)

            return data

    class VolumeTitlePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.chapter_title:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            chaptertitle = ET.Element('volume_title')

            chaptertitle.text = raw.chapter_title

            xml.find('.').append(chaptertitle)

            return data

    class EditionPipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.edition:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            edition = ET.Element('edition_number')

            edition.text = raw.edition

            xml.find('.').append(edition)

            return data

    class DatePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.date:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            pdate = ET.Element('cYear')
            pdate.text = raw.date[0:4]

            xml.find('.').append(pdate)

            return data

    class ISSNPipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.issn:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            issn = ET.Element('issn')

            issn.text = raw.issn

            xml.find('.').append(issn)

            return data

    class ISBNPipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.isbn:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            isbn = ET.Element('isbn')

            isbn.text = raw.isbn

            xml.find('.').append(isbn)

            return data

    class StartPagePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.start_page:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            fpage = ET.Element('first_page')
            fpage.text = raw.start_page
            xml.find('.').append(fpage)

            return data

    class IssuePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.issue:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            issue = ET.Element('issue')
            issue.text = raw.issue
            xml.find('.').append(issue)

            return data

    class VolumePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.volume:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            volume = ET.Element('volume')
            volume.text = raw.volume
            xml.find('.').append(volume)

            return data

    class JournalTitlePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.source or not raw.publication_type == 'article':
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            journaltitle = ET.Element('journal_title')

            journaltitle.text = raw.source

            xml.find('.').append(journaltitle)

            return data

    class ThesisTitlePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.thesis_title:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            source = ET.Element('series_title')

            source.text = raw.thesis_title

            xml.find('.').append(source)

            return data

    class AuthorPipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.authors:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            if raw.authors and len(raw.authors) > 0:
                persongroup = ET.Element('author')
                persongroup.text = ' '.join(
                    [
                        raw.authors[0].get('surname', ''),
                        raw.authors[0].get('given_names', '')
                    ]
                )
                xml.find('.').append(persongroup)

            return data

    def deploy(self, raw):

        transformed_data = self._ppl.run(raw, rewrap=True)

        return next(transformed_data)


class XMLClosePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        data = ET.tostring(
            xml, encoding="utf-8", method="xml", xml_declaration=True)

        return data
