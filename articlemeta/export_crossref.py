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


class XMLClosePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        data = ET.tostring(
            xml, encoding="utf-8", method="xml", xml_declaration=True)

        return data
