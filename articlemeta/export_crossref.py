# coding: utf-8
from lxml import etree as ET
import re
import os
import uuid
from copy import deepcopy
from datetime import datetime

from xylose.scielodocument import UnavailableMetadataException
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

        if raw.journal.electronic_issn:
            el = ET.Element('issn')
            el.text = raw.journal.electronic_issn
            el.set('media_type', 'electronic')
            xml.find('./body/journal/journal_metadata').append(el)

        if raw.journal.print_issn:
            el = ET.Element('issn')
            el.text = raw.journal.print_issn
            el.set('media_type', 'print')
            xml.find('./body/journal/journal_metadata').append(el)

        return data


class XMLJournalIssuePipe(plumber.Pipe):
    def precond(data):
        raw, xml = data
        try:
            if raw.issue.is_ahead_of_print:
                raise plumber.UnmetPrecondition()
        except UnavailableMetadataException as e:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data
        el = ET.Element('journal_issue')
        xml.find('./body/journal').append(el)

        return data


def journal_issue_exists(data):
    raw, xml = data
    if xml.find('./body/journal/journal_issue') is None:
        raise plumber.UnmetPrecondition()


class XMLPubDatePipe(plumber.Pipe):
    @plumber.precondition(journal_issue_exists)
    def transform(self, data):
        raw, xml = data

        el = ET.Element('publication_date', media_type='online')
        date = raw.issue_publication_date  # ver export.CustomArticle

        # Month
        if date[5:7]:
            month = ET.Element('month')
            month.text = date[5:7]
            el.append(month)
        # Day
        if date[8:10]:
            day = ET.Element('day')
            day.text = date[8:10]
            el.append(day)
        # Year
        if date[0:4]:
            year = ET.Element('year')
            year.text = date[0:4]
            el.append(year)

        xml.find('./body/journal/journal_issue').append(el)

        return data


class XMLVolumePipe(plumber.Pipe):

    def precond(data):
        raw, xml = data
        try:
            if not raw.issue.volume:
                raise plumber.UnmetPrecondition()
        except UnavailableMetadataException as e:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    @plumber.precondition(journal_issue_exists)
    def transform(self, data):
        raw, xml = data

        volume = ET.Element('volume')
        volume.text = raw.issue.volume

        el = ET.Element('journal_volume')
        el.append(volume)

        xml.find('./body/journal/journal_issue').append(el)

        return data


class XMLIssuePipe(plumber.Pipe):

    def precond(data):
        raw, xml = data
        try:
            if not raw.issue:
                raise plumber.UnmetPrecondition()
        except UnavailableMetadataException as e:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    @plumber.precondition(journal_issue_exists)
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

        journal = xml.find('./body/journal')
        for item in raw.doi_and_lang:
            el = ET.Element('journal_article')
            el.set('language', item[0])
            el.set('publication_type', 'full_text')
            el.set('reference_distribution_opts', 'any')
            journal.append(el)
        return data


class XMLArticleTitlesPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data
        el = ET.Element('titles')
        for ja in xml.findall('.//journal_article'):
            ja.append(deepcopy(el))
        return data


class XMLArticleTitlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data
        nodes = xml.findall('.//journal_article')

        for ja, doi_and_lang in zip(nodes, raw.doi_and_lang):
            node = ja.find('./titles')
            el = ET.Element('title')
            lang, doi = doi_and_lang
            if lang == raw.original_language():
                # el.set('language', lang)
                el.text = raw.original_title() or '[NO TITLE AVAILABLE]'
                node.append(el)
            else:
                el.text = raw.translated_titles().get(lang) or '[NO TITLE AVAILABLE]'
                el_original = ET.Element('original_language_title')
                el_original.set('language', raw.original_language())
                el_original.text = raw.original_title()
                node.append(el)
                node.append(el_original)
        return data


class XMLArticleContributorsPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.authors:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        el = ET.Element('contributors')
        for ndx, authors in enumerate(raw.authors):
            author = ET.Element('person_name')
            author.set('contributor_role', 'author')

            seq = 'first' if ndx == 0 else 'additional'
            author.set('sequence', seq)
            el.append(author)

            if 'given_names' in authors and authors['given_names']:
                firstname = ET.Element('given_name')
                firstname.text = authors['given_names']
                author.append(firstname)

            if 'surname' in authors and authors['surname']:
                lastname = ET.Element('surname')
                author_surname = authors['surname'].split()
                if len(author_surname) > 1 and \
                        raw.is_name_suffix(author_surname[-1]): # ver export.CustomArticle
                    suffix = ET.Element('suffix')
                    suffix.text = author_surname[-1]
                    lastname.text = " ".join(author_surname[:-1])
                    author.append(lastname)
                    author.append(suffix)
                else:
                    lastname.text = authors['surname']
                    author.append(lastname)

            author_index = [i.upper() for i in authors.get('xref', []) or []]

            if raw.affiliations:
                affs_list = []
                for aff in raw.affiliations:
                    affiliation = ET.Element('affiliation')
                    if 'index' not in aff:
                        continue
                    if aff['index'].upper() in author_index:
                        aff_list = []
                        if 'institution' in aff:
                            aff_list.append(aff['institution'])
                        if 'addr_line' in aff:
                            aff_list.append(aff['addr_line'])
                        if 'country' in aff:
                            aff_list.append(aff['country'])

                        aff_info = ',  '.join(aff_list)
                        if len(aff_info.strip()) == 0:
                            continue
                        affs_list.append(aff_info)

                affs = '; '.join(affs_list)
                if len(affs) > 0:
                    affiliation.text = affs
                    author.append(affiliation)

            if 'orcid' in authors and authors['orcid']:
                orcid = ET.Element('ORCID')
                orcid.text = 'http://orcid.org/%s' % authors['orcid']
                author.append(orcid)

        for journal_article in xml.findall('./body/journal//journal_article'):
            new_el = deepcopy(el)
            journal_article.append(new_el)

        return data


class XMLArticleAbstractPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.original_abstract() or not raw.translated_abstracts():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        abstract = None
        if raw.original_abstract():
            paragraph = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}p')
            paragraph.text = raw.original_abstract()
            abstract = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}abstract')
            abstract.set('{http://www.w3.org/XML/1998/namespace}lang', raw.original_language())
            abstract.append(paragraph)

        translated_abstracts = []
        for language, body in raw.translated_abstracts().items():
            paragraph = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}p')
            paragraph.text = body
            el = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}abstract')
            el.set('{http://www.w3.org/XML/1998/namespace}lang', language)
            el.append(paragraph)
            translated_abstracts.append(el)

        for journal_article in xml.findall('./body/journal//journal_article'):
            if abstract is not None:
                journal_article.append(deepcopy(abstract))
            for item in translated_abstracts:
                journal_article.append(deepcopy(item))
        return data


class XMLArticlePubDatePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        date = raw.publication_date

        el = ET.Element('publication_date')
        el.set('media_type', "online")

        # Month
        if date[5:7]:
            month = ET.Element('month')
            month.text = date[5:7]
            el.append(month)
        # Day
        if date[8:10]:
            day = ET.Element('day')
            day.text = date[8:10]
            el.append(day)
        # Year
        if date[0:4]:
            year = ET.Element('year')
            year.text = date[0:4]
            el.append(year)

        for journal_article in xml.findall('./body/journal//journal_article'):
            journal_article.append(deepcopy(el))

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

        for journal_article in xml.findall('./body/journal//journal_article'):
            journal_article.append(deepcopy(el))

        return data


class XMLPIDPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        identifier = ET.Element('identifier')
        identifier.set('id_type',  'pii')
        identifier.text = raw.publisher_id

        el = ET.Element('publisher_item')
        el.append(identifier)

        for journal_article in xml.findall('./body/journal//journal_article'):
            journal_article.append(deepcopy(el))

        return data


class XMLDOIDataPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        el = ET.Element('doi_data')

        for journal_article in xml.findall('./body/journal//journal_article'):
            journal_article.append(deepcopy(el))

        return data


class XMLDOIPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        nodes = xml.findall('./body/journal//journal_article/doi_data')
        for doi_data_elem, doi_and_lang in zip(nodes, raw.doi_and_lang):
            doi = ET.Element('doi')
            doi.text = doi_and_lang[1]
            doi_data_elem.append(doi)

        return data


class XMLResourcePipe(plumber.Pipe):

    ARTICLE_URL = 'http://{}/scielo.php?script=sci_arttext&pid={}&tlng={}'

    def precond(data):
        raw, xml = data
        try:
            if not raw.scielo_domain or not raw.publisher_id:
                raise plumber.UnmetPrecondition()
        except:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        nodes = xml.findall('./body/journal//journal_article/doi_data')
        for doi_data_elem, doi_and_lang in zip(nodes, raw.doi_and_lang):
            resource = ET.Element('resource')
            resource.text = self.ARTICLE_URL.format(
                    raw.scielo_domain, raw.publisher_id, doi_and_lang[0]
                )
            doi_data_elem.append(resource)

        return data


class XMLCollectionPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.fulltexts().get('pdf', None):
            raise plumber.UnmetPrecondition()

    def create_collection_element(self, resource_value):
        resource = ET.Element('resource')
        resource.text = resource_value

        item = ET.Element('item')
        item.set('crawler', 'iParadigms')
        item.append(resource)

        collection = ET.Element('collection')
        collection.set('property', 'crawler-based')
        collection.append(item)
        return collection

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data
        pdf_items = raw.fulltexts().get('pdf')
        for doi_data, doi_and_lang in zip(
                xml.findall('.//journal_article/doi_data'),
                raw.doi_and_lang):
            collection = self.create_collection_element(
                pdf_items.get(doi_and_lang[0]))
            doi_data.append(collection)

        return data


class XMLArticleCitationsPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.citations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        citations = ET.Element('citation_list')

        cit = XMLCitation()
        for citation in raw.citations:
            citations.append(cit.deploy(citation)[1])

        for ja in xml.findall('.//journal_article'):
            ja.append(deepcopy(citations))

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


class XMLProgramPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data
        data = self._transform_original(data)
        data = self._transform_translations(data)
        return data

    def _transform_original(self, data):
        raw, xml = data

        journal_article_node = xml.find('.//journal_article')

        doi_and_lang = raw.doi_and_lang[1:]

        # program
        program_node = ET.Element('program')
        program_node.set('xmlns',  'http://www.crossref.org/relations.xsd')

        translated_titles = raw.translated_titles()
        for lang, doi in doi_and_lang:

            # program/related_item
            related_item_node = ET.Element('related_item')

            # program/related_item/description
            description_node = ET.Element('description')
            description_node.text = translated_titles.get(lang)
            related_item_node.append(description_node)

            # program/related_item/intra_work_relation
            intra_work_relation_node = ET.Element('intra_work_relation')
            intra_work_relation_node.set(
                'relationship-type', 'isTranslationOf')
            intra_work_relation_node.set('identifier-type', 'doi')
            intra_work_relation_node.text = doi
            related_item_node.append(intra_work_relation_node)

            program_node.append(related_item_node)

        journal_article_node.append(program_node)

        return data

    def _transform_translations(self, data):
        raw, xml = data

        # program
        program_node = ET.Element('program')
        program_node.set('xmlns',  'http://www.crossref.org/relations.xsd')

        # program/related_item
        related_item_node = ET.Element('related_item')

        # program/related_item/description
        description_node = ET.Element('description')
        description_node.text = raw.original_title()
        related_item_node.append(description_node)

        # program/related_item/intra_work_relation
        intra_work_relation_node = ET.Element('intra_work_relation')
        intra_work_relation_node.set(
            'relationship-type', 'isTranslationOf')
        intra_work_relation_node.set('identifier-type', 'doi')
        intra_work_relation_node.text = raw.doi
        related_item_node.append(intra_work_relation_node)

        program_node.append(related_item_node)

        for journal_article_node in xml.findall('.//journal_article')[1:]:
            journal_article_node.append(deepcopy(program_node))

        return data
