# coding: utf-8
import re

from lxml import etree as ET

from xylose.scielodocument import UnavailableMetadataException
import plumber

SUPPLBEG_REGEX = re.compile(r'^0 ')
SUPPLEND_REGEX = re.compile(r' 0$')

ALLOWED_LANGUAGES = ['af', 'de', 'en', 'es', 'fr', 'it', 'la', 'pt', 'po']


def create_children(root_node, tags, values):
    for tag, value in zip(tags, values):
        if value is not None or value != '':
            e = ET.Element(tag)
            e.text = value
            root_node.append(e)
    return root_node


def splited_yyyy_mm_dd(date_iso):
    if date_iso is not None:
        parts = date_iso.split('-')
        if len(parts) == 2:
            parts.append(None)
        if len(parts) == 1:
            parts.append(None)
            parts.append(None)
        if len(parts) == 3:
            return parts


def create_date_elem(element_date_name, splited_yyyy_mm_dd, date_type=None):
    if splited_yyyy_mm_dd is not None:
        y, m, d = splited_yyyy_mm_dd
        elem_date = ET.Element(element_date_name)
        if date_type is not None:
            elem_date.set('date-type', date_type)
        tags = ['day', 'month', 'year']
        values = [d, m, y]
        return create_children(elem_date, tags, values)


class XMLCitation(object):

    def __init__(self):
        self._ppl = plumber.Pipeline(self.SetupCitationPipe(),
                                     self.RefIdPipe(),
                                     self.ElementCitationPipe(),
                                     self.ArticleTitlePipe(),
                                     self.ThesisTitlePipe(),
                                     self.ConferencePipe(),
                                     self.LinkTitlePipe(),
                                     self.SourcePipe(),
                                     self.DatePipe(),
                                     self.StartPagePipe(),
                                     self.EndPagePipe(),
                                     self.IssuePipe(),
                                     self.VolumePipe(),
                                     self.PersonGroupPipe(),
                                     self.URIPipe()
                                     )

    class SetupCitationPipe(plumber.Pipe):

        def transform(self, data):

            xml = ET.Element('ref')

            return data, xml

    class RefIdPipe(plumber.Pipe):
        def transform(self, data):
            raw, xml = data

            ref = xml.find('.')

            ref.set('id', 'B{0}'.format(str(raw.index_number)))

            return data

    class ElementCitationPipe(plumber.Pipe):
        def transform(self, data):
            raw, xml = data
            elementcitation = ET.Element('element-citation')
            elementcitation.set('publication-type', raw.publication_type)
            xml.find('.').append(elementcitation)
            return data

    class ArticleTitlePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.article_title:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            articletitle = ET.Element('article-title')

            articletitle.text = raw.article_title

            xml.find('./element-citation').append(articletitle)

            return data

    class SourcePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.source:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            source = ET.Element('source')

            source.text = raw.source

            xml.find('./element-citation').append(source)

            return data

    class ThesisTitlePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.thesis_title:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            source = ET.Element('source')

            source.text = raw.thesis_title

            xml.find('./element-citation').append(source)

            return data

    class ConferencePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if raw.publication_type != 'conference':
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            elem_cit = xml.find('./element-citation')
            if raw.conference_name != '':
                conf_name = ET.Element('conf-name')
                conf_name.text = raw.conference_name
                elem_cit.append(conf_name)
            if raw.conference_location != '':
                conf_location = ET.Element('conf-loc')
                conf_location.text = raw.conference_location
                elem_cit.append(conf_location)

            return data

    class LinkTitlePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.link_title:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            source = ET.Element('source')

            source.text = raw.link_title

            xml.find('./element-citation').append(source)

            return data

    class URIPipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.link:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            elem_citation = xml.find('./element-citation')

            elem = ET.Element('ext-link')
            elem.set('ext-link-type', 'uri')
            elem.set('href', raw.link)
            elem.text = raw.link
            elem_citation.append(elem)

            try:
                access_date = raw.access_date
            except AttributeError:
                access_date = raw.date
            if access_date is not None:
                date_in_citation_elem = create_date_elem(
                    'date-in-citation',
                    splited_yyyy_mm_dd(access_date)
                )
                if date_in_citation_elem is not None:
                    elem_citation.append(date_in_citation_elem)

            return data

    class DatePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.date:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            pdate = ET.Element('date')

            if raw.date[8:10]:
                day = ET.Element('day')
                day.text = raw.date[8:10]
                pdate.append(day)

            if raw.date[5:7]:
                month = ET.Element('month')
                month.text = raw.date[5:7]
                pdate.append(month)

            year = ET.Element('year')
            year.text = raw.date[0:4]
            pdate.append(year)

            xml.find('./element-citation').append(pdate)

            return data

    class StartPagePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.start_page:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            fpage = ET.Element('fpage')
            fpage.text = raw.start_page
            xml.find('./element-citation').append(fpage)

            return data

    class EndPagePipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.end_page:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            lpage = ET.Element('lpage')
            lpage.text = raw.end_page
            xml.find('./element-citation').append(lpage)

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
            xml.find('./element-citation').append(issue)

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
            xml.find('./element-citation').append(volume)

            return data

    class PersonGroupPipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            try:
                if not raw.authors_groups:
                    raise plumber.UnmetPrecondition()
            except AttributeError:
                conditions = [
                    raw.authors,
                    raw.monographic_authors,
                    raw.data.get('v11'),
                    raw.data.get('v17')
                ]
                if any(conditions) is False:
                    raise plumber.UnmetPrecondition()

        def _create_author(self, author):
            if not isinstance(author, dict):
                element = ET.Element('collab')
                element.text = author
                return element
            element = ET.Element('name')
            _surname = author.get('surname')
            _given_names = author.get('given_names')
            if _surname == '' and _given_names:
                _surname = _given_names
                _given_names = ''
            if _surname != '':
                surname = ET.Element('surname')
                surname.text = _surname
                element.append(surname)
            if _given_names != '':
                givennames = ET.Element('given-names')
                givennames.text = _given_names
                element.append(givennames)
            return element

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data
            try:
                data = self._transform_authors_groups(data)
            except AttributeError:
                # caso não exista raw.authors_groups
                data = self._transform_authors(data)
            return data

        def _transform_authors_groups(self, data):
            raw, xml = data
            if raw.authors_groups:
                elem_citation = xml.find('./element-citation')
                groups = raw.authors_groups
                for group in ['analytic', 'monographic']:
                    author_group = groups.get(group)
                    if author_group is not None:
                        persongroup = ET.Element('person-group')
                        for author_type, authors in author_group.items():
                            for author in authors:
                                persongroup.append(self._create_author(author))
                        elem_citation.append(persongroup)
            return data

        def _transform_authors(self, data):
            raw, xml = data
            analytics = raw.analytic_authors or []
            analytics += raw.analytic_institution or []
            if raw.analytic_institution is None and \
                    raw.data.get('v11') is not None:
                for institution in raw.data.get('v11', []):
                    analytics.append(institution['_'])
            aa = []
            for author in analytics:
                aa.append(self._create_author(author))

            monographic = raw.monographic_authors or []
            monographic += raw.monographic_institution or []
            if raw.monographic_institution is None and \
                    raw.data.get('v17') is not None:
                for institution in raw.data.get('v17', []):
                    monographic.append(institution['_'])
            ma = []
            for author in monographic:
                ma.append(self._create_author(author))

            author_groups = []
            if aa:
                author_groups.append(aa)
            if ma:
                author_groups.append(ma)

            elem_citation = xml.find('./element-citation')
            for author_group in author_groups:
                persongroup = ET.Element('person-group')
                for author in author_group:
                    persongroup.append(author)
                elem_citation.append(persongroup)

            return data

    def deploy(self, raw):

        transformed_data = self._ppl.run(raw, rewrap=True)

        return next(transformed_data)


class SetupArticlePipe(plumber.Pipe):

    def transform(self, data):

        nsmap = {
            'xml': 'http://www.w3.org/XML/1998/namespace'
        }

        xml = ET.Element('articles', nsmap=nsmap)
        xml.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', 'https://raw.githubusercontent.com/scieloorg/articles_meta/master/tests/xsd/scielo_sci/ThomsonReuters_publishing.xsd')
        xml.set('dtd-version', '1.10')

        return data, xml


class XMLArticlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        lang_id = raw.original_language() if raw.original_language() in ALLOWED_LANGUAGES else 'zz'

        article = ET.Element('article')
        article.set('lang_id', lang_id)
        article.set('article-type', raw.document_type)

        xml.append(article)

        return data


class XMLFrontPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        article = xml.find('article')
        article.append(ET.Element('front'))

        front = article.find('front')
        front.append(ET.Element('journal-meta'))
        front.append(ET.Element('article-meta'))

        return data


class XMLJournalMetaJournalIdPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        journalid = ET.Element('journal-id')
        journalid.text = raw.journal.acronym
        journalid.set('journal-id-type', 'publisher')

        xml.find('./article/front/journal-meta').append(journalid)

        return data


class XMLJournalMetaJournalTitleGroupPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        journaltitle = ET.Element('journal-title')
        journaltitle.text = raw.journal.title

        journalabbrevtitle = ET.Element('abbrev-journal-title')
        journalabbrevtitle.text = raw.journal.abbreviated_title

        journaltitlegroup = ET.Element('journal-title-group')
        journaltitlegroup.append(journaltitle)
        journaltitlegroup.append(journalabbrevtitle)

        xml.find('./article/front/journal-meta').append(journaltitlegroup)

        return data


class XMLJournalMetaISSNPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        issn = ET.Element('issn')
        issn.text = raw.any_issn()

        xml.find('./article/front/journal-meta').append(issn)

        return data


class XMLJournalMetaCollectionPipe(plumber.Pipe):
    def precond(data):

        raw, xml = data

        if not raw.collection_acronym:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        collection = ET.Element('collection')

        collection.text = 'SciELO %s' % raw.collection_name

        xml.find('./article/front/journal-meta').append(collection)

        return data


class XMLJournalMetaPublisherPipe(plumber.Pipe):
    def transform(self, data):
        return self.join_publisher_names(data, '; ')

    def join_publisher_names(self, data, separator='; '):
        raw, xml = data
        publisher_names = separator.join(raw.journal.publisher_name or [])

        publishername = ET.Element('publisher-name')
        publishername.text = publisher_names

        publisher = ET.Element('publisher')
        publisher.append(publishername)

        xml.find('./article/front/journal-meta').append(publisher)

        return data

    def get_first_publisher_name(self, data):
        raw, xml = data
        publisher_names = raw.journal.publisher_name or []
        if len(publisher_names) > 0:
            publishername = ET.Element('publisher-name')
            publishername.text = publisher_names[0]
            publisher = ET.Element('publisher')
            publisher.append(publishername)
            xml.find('./article/front/journal-meta').append(publisher)
        return data


class XMLArticleMetaUniqueArticleIdPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        uniquearticleid = ET.Element('unique-article-id')
        uniquearticleid.set('pub-id-type', 'publisher-id')
        uniquearticleid.text = raw.publisher_id

        xml.find('./article/front/article-meta').append(uniquearticleid)

        return data


class XMLArticleMetaArticleIdPublisherPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        articleidpublisher = ET.Element('article-id')
        articleidpublisher.set('pub-id-type', 'publisher-id')
        articleidpublisher.text = raw.publisher_id

        xml.find('./article/front/article-meta').append(articleidpublisher)

        return data


class XMLArticleMetaArticleIdDOIPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.doi:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        articleiddoi = ET.Element('article-id')
        articleiddoi.set('pub-id-type', 'doi')
        articleiddoi.text = raw.doi

        xml.find('./article/front/article-meta').append(articleiddoi)

        return data


class XMLArticleMetaArticleCategoriesPipe(plumber.Pipe):
    def precond(data):

        raw, xml = data

        if not raw.journal.wos_subject_areas:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        subjectgroup = ET.Element('subj-group')

        for subject in raw.journal.wos_subject_areas:
            sbj = ET.Element('subject')
            sbj.text = subject
            subjectgroup.append(sbj)

        articlecategories = ET.Element('article-categories')
        articlecategories.append(subjectgroup)

        xml.find('./article/front/article-meta').append(articlecategories)

        return data


class XMLArticleMetaTitleGroupPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        lang_id = raw.original_language() if raw.original_language() in ALLOWED_LANGUAGES else 'zz'

        articletitle = ET.Element('article-title')
        articletitle.set('lang_id', lang_id)

        articletitle.text = raw.original_title()

        titlegroup = ET.Element('title-group')
        titlegroup.append(articletitle)

        xml.find('./article/front/article-meta').append(titlegroup)

        return data


class XMLArticleMetaTranslatedTitleGroupPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.translated_titles():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for lang, title in raw.translated_titles().items():
            transtitle = ET.Element('trans-title')
            transtitle.text = title
            lang_id = lang if lang in ALLOWED_LANGUAGES else 'zz'
            transtitlegrp = ET.Element('trans-title-group')
            transtitlegrp.set('lang_id', lang_id)
            transtitlegrp.append(transtitle)

            xml.find('./article/front/article-meta/title-group').append(transtitlegrp)

        return data


class XMLArticleMetaContribGroupPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.authors:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        contribgroup = ET.Element('contrib-group')

        for author in raw.authors:
            contribname = ET.Element('name')

            if 'surname' in author:
                contribsurname = ET.Element('surname')
                contribsurname.text = author['surname']
                contribname.append(contribsurname)

            if 'given_names' in author:
                contribgivennames = ET.Element('given-names')
                contribgivennames.text = author['given_names']
                contribname.append(contribgivennames)

            role = ET.Element('role')
            role.text = author.get('role', 'ND')

            contrib = ET.Element('contrib')
            contrib.set('contrib-type', 'author')
            contrib.append(contribname)
            contrib.append(role)

            for xr in author.get('xref', []):
                xref = ET.Element('xref')
                xref.set('ref-type', 'aff')
                xref.set('rid', xr.upper())
                contrib.append(xref)

            contribgroup.append(contrib)

        xml.find('./article/front/article-meta').append(contribgroup)

        return data


class XMLArticleMetaAffiliationPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.mixed_affiliations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for affiliation in raw.mixed_affiliations:

            aff = ET.Element('aff')
            aff.set('id', affiliation['index'].upper())

            if 'institution' in affiliation:
                institution = ET.Element('institution')
                institution.text = affiliation['institution']
                aff.append(institution)

            if 'country' in affiliation:
                country = ET.Element('country')
                country.text = affiliation['country']
                aff.append(country)

            xml.find('./article/front/article-meta').append(aff)

        return data


class XMLArticleMetaDatesInfoPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.publication_date:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        pubdate = ET.Element('pub-date')

        year = ET.Element('year')
        year.text = raw.publication_date[0:4]

        if raw.publication_date[5:7]:
            month = ET.Element('month')
            month.text = raw.publication_date[5:7]
            pubdate.append(month)

        pubdate.append(year)

        articlemeta = xml.find('./article/front/article-meta')
        articlemeta.append(pubdate)

        return data


class XMLArticleMetaPagesInfoPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        fpage = ET.Element('fpage')
        fpage.text = raw.start_page

        lpage = ET.Element('lpage')
        lpage.text = raw.end_page

        articlemeta = xml.find('./article/front/article-meta')

        if raw.start_page:
            articlemeta.append(fpage)
        if raw.end_page:
            articlemeta.append(lpage)

        return data


class XMLArticleMetaElocationInfoPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.elocation:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        elocation = ET.Element('elocation-id')
        elocation.text = raw.elocation

        articlemeta = xml.find('./article/front/article-meta')
        articlemeta.append(elocation)

        return data


class XMLArticleMetaIssueInfoPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        try:
            if not raw.issue:
                raise plumber.UnmetPrecondition()
        except UnavailableMetadataException as e:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
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

        articlemeta = xml.find('./article/front/article-meta')

        if label_volume:
            vol = ET.Element('volume')
            vol.text = label_volume.strip()
            articlemeta.append(vol)

        if label_issue:
            issue = ET.Element('issue')
            issue.text = label_issue.strip()        
            articlemeta.append(issue)

        return data


class XMLArticleMetaURLsPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        articlemeta = xml.find('./article/front/article-meta')

        try:
            if raw.issue.url(language='en'):
                issue_uri = ET.Element('self-uri')
                issue_uri.set('href', raw.issue.url(language='en'))
                issue_uri.set('content-type', 'issue_page')
                articlemeta.append(issue_uri)
        except UnavailableMetadataException:
            pass

        if raw.journal.url(language='en'):
            journal_uri = ET.Element('self-uri')
            journal_uri.set('href', raw.journal.url(language='en'))
            journal_uri.set('content-type', 'journal_page')
            articlemeta.append(journal_uri)

        if raw.html_url(language='en'):
            article_uri = ET.Element('self-uri')
            article_uri.set('href', raw.html_url(language='en'))
            article_uri.set('content-type', 'full_text_page')
            articlemeta.append(article_uri)

        return data


class XMLArticleMetaAbstractsPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        p = ET.Element('p')
        p.text = raw.original_abstract()

        lang_id = raw.original_language() if raw.original_language() in ALLOWED_LANGUAGES else 'zz'

        abstract = ET.Element('abstract')
        abstract.set('lang_id', lang_id)
        abstract.append(p)

        articlemeta = xml.find('./article/front/article-meta')

        if raw.original_abstract():
            articlemeta.append(abstract)

        if raw.translated_abstracts():
            for lang, text in raw.translated_abstracts().items():
                p = ET.Element('p')
                p.text = text
                lang_id = lang if lang in ALLOWED_LANGUAGES else 'zz'
                abstract = ET.Element('trans-abstract')
                abstract.set('lang_id', lang)
                abstract.append(p)

                articlemeta.append(abstract)

        return data


class XMLArticleMetaKeywordsPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.keywords():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        articlemeta = xml.find('./article/front/article-meta')

        for lang, keywords in raw.keywords().items():
            kwdgroup = ET.Element('kwd-group')
            lang_id = lang if lang in ALLOWED_LANGUAGES else 'zz'
            kwdgroup.set('lang_id', lang_id)
            kwdgroup.set('kwd-group-type', 'author-generated')
            for keyword in keywords:
                kwd = ET.Element('kwd')
                kwd.text = keyword
                kwdgroup.append(kwd)
            articlemeta.append(kwdgroup)

        return data


class XMLArticleMetaPermissionPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.permissions:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        articlemeta = xml.find('./article/front/article-meta')

        permissions = ET.Element('permissions')
        dlicense = ET.Element('license')
        dlicense.set('license-type', 'open-access')
        dlicense.set('href', raw.permissions['url'])

        licensep = ET.Element('license-p')
        licensep.text = raw.permissions['text']

        dlicense.append(licensep)
        permissions.append(dlicense)
        articlemeta.append(permissions)

        return data


class XMLArticleMetaCitationsPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.citations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        article = xml.find('./article')
        article.append(ET.Element('back'))

        back = article.find('back')
        back.append(ET.Element('ref-list'))

        reflist = xml.find('./article/back/ref-list')

        cit = XMLCitation()
        for citation in raw.citations:
            reflist.append(cit.deploy(citation)[1])

        return data


class XMLClosePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        data = ET.tostring(xml, encoding="utf-8", method="xml")

        return data
