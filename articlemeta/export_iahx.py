#coding: utf-8
import xml.etree.ElementTree as ET

import plumber


class SetupDocumentPipe(plumber.Pipe):

    def transform(self, data):
        xml = ET.Element('doc')

        return data, xml


class XMLDocumentIDPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = 'art-{0}-{1}'.format(raw.publisher_id, raw.collection_acronym)
        field.set('name', 'id')

        xml.find('.').append(field)

        return data


class XMLCollectionPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.collection_acronym
        field.set('name', 'in')

        xml.find('.').append(field)

        return data


class XMLKnowledgeAreaPipe(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.subject_areas:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for item in raw.subject_areas:
            field = ET.Element('field')
            field.text = item
            field.set('name', 'ac')

            xml.find('.').append(field)

        return data


class XMLCenterPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = 'br1.1'
        field.set('name', 'cc')

        xml.find('.').append(field)

        return data


class XMLDocumentTypePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.document_type
        field.set('name', 'type')

        xml.find('.').append(field)

        return data


class XMLURPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = 'art-{0}'.format(raw.publisher_id)
        field.set('name', 'ur')

        xml.find('.').append(field)

        return data


class XMLAuthorsPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.authors:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for author in raw.authors:
            field = ET.Element('field')
            name = []
            if 'given_names' in author:
                name.append(author['given_names'])

            if 'surname' in author:
                name.append(author['surname'])

            field.text = ', '.join(name)

            field.set('name', 'au')
            xml.find('.').append(field)

        return data


class XMLTitlePipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.original_title() and not raw.translated_titles():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.original_title()
        field.set('name', 'ti_%s' % raw.original_language())
        xml.find('.').append(field)

        if not raw.translated_titles():
            return data

        for language, title in raw.translated_titles().items():
            field = ET.Element('field')
            field.text = title
            field.set('name', 'ti_%s' % language)
            xml.find('.').append(field)

        return data


class XMLPagesPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.start_page and not raw.end_page:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        pages = []

        if raw.start_page:
            pages.append(raw.start_page)

        if raw.end_page:
            pages.append(raw.end_page)

        field = ET.Element('field')
        field.text = '-'.join(pages)
        field.set('name', 'pg')
        xml.find('.').append(field)

        return data


class XMLDOIPipe(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.doi:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.doi.upper().replace('HTTP://DX.DOI.ORG/', '')
        field.set('name', 'doi')
        xml.find('.').append(field)

        return data


class XMLWOKCIPipe(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.wos_citation_indexes:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for index in raw.wos_citation_indexes:
            field = ET.Element('field')
            field.text = index.replace('&', '')
            field.set('name', 'wok_citation_index')
            xml.find('.').append(field)

        return data


class XMLWOKSCPipe(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.wos_subject_areas:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for index in raw.wos_subject_areas:
            field = ET.Element('field')
            field.text = index
            field.set('name', 'wok_subject_categories')
            xml.find('.').append(field)

        return data


class XMLIssueLabelPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        label = []
        if raw.journal_abbreviated_title:
            label.append(raw.journal_abbreviated_title)

        issue = "{0}{1}({2}{3})".format(raw.volume or '', raw.supplement_volume or '', raw.issue or '', raw.supplement_issue or '')
        label.append(issue)

        pages = []

        if raw.start_page:
            pages.append(raw.start_page)

        if raw.end_page:
            pages.append(raw.end_page)

        label.append('-'.join(pages))

        label.append(raw.publication_date)

        field = ET.Element('field')
        field.text = '; '.join(label)
        field.set('name', 'fo')
        xml.find('.').append(field)

        return data


class XMLJournalTitlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.journal_title
        field.set('name', 'journal_title')
        xml.find('.').append(field)

        return data


class XMLJournalAbbrevTitlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.journal_abbreviated_title
        field.set('name', 'ta')
        xml.find('.').append(field)

        return data


class XMLOriginalLanguagePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.original_language()
        field.set('name', 'la')
        xml.find('.').append(field)

        return data


class XMLPublicationDatePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.publication_date
        field.set('name', 'da')
        xml.find('.').append(field)

        return data


class XMLAbstractPipe(plumber.Pipe):

    def precond(data):
        raw, xml = data

        if not raw.original_abstract() and not raw.translated_abstracts():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        field = ET.Element('field')
        field.text = raw.original_abstract()
        field.set('name', 'ab_%s' % raw.original_language())
        xml.find('.').append(field)

        if not raw.translated_abstracts():
            return data

        for language, abstract in raw.translated_abstracts().items():
            field = ET.Element('field')
            field.text = abstract
            field.set('name', 'ab_%s' % language)
            xml.find('.').append(field)

        return data


class XMLAffiliationCountryPipe(plumber.Pipe):

    def precond(data):
        raw, xml = data
        if not raw.mixed_affiliations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        countries = set()

        for affiliation in raw.mixed_affiliations:
            if 'country' in affiliation:
                countries.add(affiliation['country'])

        for country in countries:
            field = ET.Element('field')
            field.text = country.strip()
            field.set('name', 'aff_country')
            xml.find('.').append(field)

        return data


class XMLAffiliationInstitutionPipe(plumber.Pipe):

    def precond(data):
        raw, xml = data
        if not raw.mixed_affiliations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        institutions = set()

        for affiliation in raw.mixed_affiliations:
            if 'institution' in affiliation:
                institutions.add(affiliation['institution'])

        for institution in institutions:
            field = ET.Element('field')
            field.text = institution.strip()
            field.set('name', 'aff_institution')
            xml.find('.').append(field)

        return data


class XMLSponsorPipe(plumber.Pipe):

    def precond(data):
        raw, xml = data
        if not raw.project_sponsor:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        sponsors = set()

        for sponsor in raw.project_sponsor:
            if 'orgname' in sponsor:
                sponsors.add(sponsor['orgname'])

        for sponsor in sponsors:
            field = ET.Element('field')
            field.text = sponsor
            field.set('name', 'sponsor')
            xml.find('.').append(field)

        return data


class XMLTearDownPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        return xml
