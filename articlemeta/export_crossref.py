# coding: utf-8
from lxml import etree as ET
import re
import os
import uuid
from copy import deepcopy
from datetime import datetime
from itertools import product

from xylose.scielodocument import UnavailableMetadataException
import plumber

SUPPLBEG_REGEX = re.compile(r'^0 ')
SUPPLEND_REGEX = re.compile(r' 0$')


class SetupDoiBatchPipe(plumber.Pipe):

    def transform(self, data):

        nsmap = {
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'jats': 'http://www.ncbi.nlm.nih.gov/JATS1',
            'xml': 'http://www.w3.org/XML/1998/namespace',
            'ai': 'http://www.crossref.org/AccessIndicators.xsd',
            'fr': 'http://www.crossref.org/fundref.xsd'
        }

        el = ET.Element('doi_batch', nsmap=nsmap)
        el.set('version', '5.3.1')
        el.set('xmlns', 'http://www.crossref.org/schema/5.3.1')
        el.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', 'http://www.crossref.org/schema/5.3.1 http://crossref.org/schemas/crossref5.3.1.xsd')

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
        raw, __ = data
        if not raw.issue:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    @plumber.precondition(journal_issue_exists)
    def transform(self, data):
        raw, xml = data

        if raw.issue.volume:
            volume = ET.Element('volume')
            volume.text = raw.issue.volume
            el = ET.Element('journal_volume')
            el.append(volume)
            xml.find('./body/journal/journal_issue').append(el)

        return data


class XMLIssuePipe(plumber.Pipe):

    def precond(data):
        raw, __ = data
        if not raw.issue:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    @plumber.precondition(journal_issue_exists)
    def transform(self, data):
        raw, xml = data

        label_issue = raw.issue.number.replace('ahead', '') if raw.issue.number else ''

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


def title_doi_lang(raw):
    items = {}

    items[raw.original_language()] = {
        "article_title": raw.original_title(),
        "doi": raw.doi,
        "original": True,
    }
    for lang, article_title in (raw.translated_titles() or {}).items():
        items[lang] = items.get(lang) or {}
        items[lang]["article_title"] = article_title

    for lang, doi in raw.doi_and_lang:
        items[lang] = items.get(lang) or {}
        items[lang]["doi"] = doi

    return items


def _get_langs_ordered_by_priority(raw):
    other_langs = list((raw.translated_titles() or {}).keys())
    article_langs = [raw.original_language()] + other_langs
    main_langs = []
    for lang in ["en", "pt", "es"] + article_langs:
        if lang in article_langs and lang not in main_langs:
            main_langs.append(lang)
    return main_langs


class XMLArticleTitlePipe(plumber.Pipe):
    """
    Create `<title>` and `<original_language_title/>`
    `<title>` contains the article title related to the corresponding DOI
    `<original_language_title>` is a title different from `<title>`, select the
    first title from a priority list: en, pt, es, other article title languages
    """

    def transform(self, data):
        raw, xml = data
        nodes = xml.findall('.//journal_article')

        article_titles = {raw.original_language(): raw.original_title()}
        article_titles.update(raw.translated_titles() or {})
        langs_ordered_by_priority = _get_langs_ordered_by_priority(raw)

        for ja in nodes:
            ja_lang = ja.get("language")

            node = ja.find('./titles')

            # create `<title>` which content is a title in a language equal to `ja_lang`
            el = ET.Element('title')
            el.text = article_titles.get(ja_lang) or '[NO TITLE AVAILABLE]'
            node.append(el)

            for lang in langs_ordered_by_priority:
                if ja_lang == lang:
                    continue

                # create `<original_language_title>` which content is
                # a title in a language different from `ja_lang`
                # (http://support.crossref.org/hc/requests/407513)
                alt_title = ET.Element('original_language_title')
                alt_title.set('language', lang)
                alt_title.text = article_titles.get(lang) or '[NO TITLE AVAILABLE]'
                node.append(alt_title)
                # select only the first title
                break

        return data


class XMLArticleContributorsPipe(plumber.Pipe):

    translate = {
        "ND": "author",
        "ed": "editor",
        "tr": "translator",
    }

    def precond(data):

        raw, xml = data

        if not raw.authors:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        """
        https://data.crossref.org/reports/help/schema_doc/4.4.2/index.html
          <xsd:enumeration value="author"/>
          <xsd:enumeration value="editor"/>
          <xsd:enumeration value="chair"/>
          <xsd:enumeration value="reviewer"/>
          <xsd:enumeration value="review-assistant"/>
          <xsd:enumeration value="stats-reviewer"/>
          <xsd:enumeration value="reviewer-external"/>
          <xsd:enumeration value="reader"/>
          <xsd:enumeration value="translator"/>
        http://data.crossref.org/reports/help/schema_doc/4.3.6/4.3.6.html
          <xsd:enumeration value="author"/>
          <xsd:enumeration value="editor"/>
          <xsd:enumeration value="chair"/>
          <xsd:enumeration value="translator"/>
        """
        raw, xml = data

        el = ET.Element('contributors')

        for ndx, authors in enumerate(raw.authors):
            author = ET.Element('person_name')
            author.set('contributor_role',
                       self.translate.get(authors.get("role"), "author"))

            seq = 'first' if ndx == 0 else 'additional'
            author.set('sequence', seq)
            el.append(author)

            if 'given_names' in authors and authors['given_names']:
                firstname = ET.Element('given_name')
                firstname.text = authors['given_names']
                author.append(firstname)

            if 'surname' in authors and authors['surname']:
                lastname = ET.Element('surname')
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

        if not raw.original_abstract():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        paragraph = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}p')
        paragraph.text = raw.original_abstract()
        abstract = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}abstract')
        abstract.set('{http://www.w3.org/XML/1998/namespace}lang', raw.original_language())
        abstract.append(paragraph)
        abstracts = {raw.original_language(): abstract}

        if raw.translated_abstracts():
            for language, body in raw.translated_abstracts().items():
                paragraph = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}p')
                paragraph.text = body
                abstract = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}abstract')
                abstract.set('{http://www.w3.org/XML/1998/namespace}lang', language)
                abstract.append(paragraph)
                abstracts[language] = abstract

        for journal_article in xml.findall('./body/journal//journal_article'):
            language = journal_article.get("language")

            journal_article.append(deepcopy(abstracts[language]))
            for lang, item in abstracts.items():
                if lang == language:
                    continue
                journal_article.append(deepcopy(item))
        return data


class XMLArticlePubDatePipe(plumber.Pipe):

    def _create_date(self, date, media_type):
        if date is not None:
            el = ET.Element('publication_date')
            el.set('media_type', media_type)
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
            return el

    def precond(data):
        raw, __ = data
        if not raw.issue:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        if raw.issue.is_ahead_of_print:
            date = raw.document_publication_date
        else:
            date = raw.issue_publication_date

        pub_date = self._create_date(date, 'online')
        if pub_date is not None:
            for journal_article in xml.findall('./body/journal//journal_article'):
                journal_article.append(deepcopy(pub_date))
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


class XMLElocationPipe(plumber.Pipe):
    """Pipeline que verifica a exisência do elocation-id (v14)
    e o adiciona no XML de formato crossref"""

    def precond(data):
        raw, _ = data

        if not raw.elocation:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        item_number = ET.Element("item_number")
        item_number.set("item_number_type", "article_number")
        item_number.text = raw.elocation

        publisher_items = xml.findall("./body/journal//journal_article//publisher_item")

        for publisher_item in publisher_items:
            publisher_item.insert(0, deepcopy(item_number))

        if not publisher_items:
            publisher_item = ET.Element("publisher_item")
            publisher_item.append(item_number)

            for journal_article in xml.findall("./body/journal//journal_article"):
                journal_article.append(deepcopy(publisher_item))

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

class XMLPermissionsPipe(plumber.Pipe):
    """Adiciona as licenças de uso ao XML para deposito do Crossref"""

    def precond(data):
        raw, _ = data

        try:
            if not raw.permissions:
                raise plumber.UnmetPrecondition()
        except UnavailableMetadataException:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        program = ET.Element(
            "{http://www.crossref.org/AccessIndicators.xsd}program"
        )
        program.set("name", "AccessIndicators")

        free_to_read = ET.Element(
            "{http://www.crossref.org/AccessIndicators.xsd}free_to_read"
        )

        program.append(free_to_read)

        if raw.permissions.get("url"):
            for context in ["vor", "am", "tdm"]:
                license_ref = ET.Element(
                    "{http://www.crossref.org/AccessIndicators.xsd}license_ref"
                )
                license_ref.set("applies_to", context)
                license_ref.text = raw.permissions.get("url")
                program.append(license_ref)

        for journal_article in xml.findall("./body/journal//journal_article"):
                journal_article.append(deepcopy(program))

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

    ARTICLE_PDF = 'http://{}/scielo.php?script=sci_pdf&pid={}&tlng={}'

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

    def transform(self, data):
        raw, xml = data

        for doi_data, doi_and_lang in zip(
                xml.findall('.//journal_article/doi_data'),
                raw.doi_and_lang):
            collection = self.create_collection_element(
                self.ARTICLE_PDF.format(
                    raw.scielo_domain, raw.publisher_id, doi_and_lang[0]
                )
            )
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

            if not raw.publication_date:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            year = raw.publication_date[0:4]

            if len(year) > 0 and year.isdigit() and int(year) > 0:
                pdate = ET.Element("cYear")
                pdate.text = year
                xml.find(".").append(pdate)

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


class XMLProgramRelatedItemPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data
        data = self._transform_original(data)
        data = self._transform_translations(data)
        return data

    def _transform_original(self, data):
        raw, xml = data

        # first journal_article (main)
        journal_article_node = xml.find('.//journal_article')

        # program
        program_node = ET.Element("program")
        program_node.set('xmlns',  'http://www.crossref.org/relations.xsd')

        original_language = raw.original_language()
        translated_titles = raw.translated_titles() or {}
        for lang, doi in raw.doi_and_lang:
            if lang == original_language:
                continue

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
        program_node = ET.Element("program")
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
            'relationship-type', 'hasTranslation')
        intra_work_relation_node.set('identifier-type', 'doi')
        intra_work_relation_node.text = raw.doi
        related_item_node.append(intra_work_relation_node)

        program_node.append(related_item_node)

        for journal_article_node in xml.findall('.//journal_article')[1:]:
            journal_article_node.append(deepcopy(program_node))

        return data

class XMLFundingDataPipe(plumber.Pipe):
    def precond(data):
        raw, _ = data
        if not raw.contract and not raw.journal.sponsors:
            raise plumber.UnmetPrecondition()

    @staticmethod
    def create_assertion(name, text):
        element = ET.Element("{http://www.crossref.org/fundref.xsd}assertion")
        element.set("name", name)
        element.text = text
        
        return element

    @staticmethod
    def create_fundgroup():
        foundgroup = ET.Element(
            "{http://www.crossref.org/fundref.xsd}assertion"
        )
        foundgroup.set("name", "fundgroup")
        return foundgroup

    def append_funding_data(self, program, sponsors=None, award_ids=None):
        if sponsors and award_ids:
            sponsors_name = [i.get("orgname") for i in sponsors if i.get("orgname")]
            for sponsor, contract in product(sponsors_name, award_ids):
                foundgroup = self.create_fundgroup()
                foundgroup.append(self.create_assertion(name="funder_name", text=sponsor))
                foundgroup.append(self.create_assertion(name="award_number", text=contract))
                program.append(foundgroup)
        elif sponsors:
            for sponsor in sponsors:
                foundgroup = self.create_fundgroup()
                foundgroup.append(self.create_assertion(name="funder_name", text=sponsor))
                program.append(foundgroup)
        elif award_ids:
            for contract in award_ids:
                foundgroup = self.create_fundgroup()
                foundgroup.append(self.create_assertion(name="award_number", text=contract))
                program.append(foundgroup)

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data
        
        program = ET.Element(
            "{http://www.crossref.org/fundref.xsd}program"
        )
        program.set("name", "fundref")
        
        self.append_funding_data(
            program=program,
            sponsors=raw.project_sponsor,
            award_ids=raw.award_ids
        )
        
        for journal_article in xml.findall(".//journal_article"):
            crossmark = journal_article.find("crossmark")

            if crossmark is not None:
                crossmark.append(program)
            else:
                journal_article.append(program)
        
        return data

