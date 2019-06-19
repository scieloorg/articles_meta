# coding: utf-8
import re

from lxml import etree as ET
from io import StringIO

import plumber

from xylose.scielodocument import UnavailableMetadataException
from articlemeta import utils

AFF_REGEX_JUST_NUMBERS = re.compile(r'\d+')
XLINK_REGEX = re.compile(r'ns\d:href')
LANG_REGEX = re.compile(r'ns\d:lang')
URI_REGEXT = re.compile(r'http://.*')
SUPPLBEG_REGEX = re.compile(r'^0 ')
SUPPLEND_REGEX = re.compile(r' 0$')


class XMLCitation(object):

    def __init__(self):
        self._ppl = plumber.Pipeline(self.SetupCitationPipe(),
                                     self.RefIdPipe(),
                                     self.MixedCitationPipe(),
                                     self.ElementCitationPipe(),
                                     self.ArticleTitlePipe(),
                                     self.ThesisTitlePipe(),
                                     self.LinkTitlePipe(),
                                     self.SourcePipe(),
                                     self.DatePipe(),
                                     self.StartPagePipe(),
                                     self.EndPagePipe(),
                                     self.IssuePipe(),
                                     self.VolumePipe(),
                                     self.PersonGroupPipe(),
                                     self.CommentPipe())

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

    class MixedCitationPipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.mixed_citation:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            parser = ET.HTMLParser()

            mc = ET.parse(StringIO(raw.mixed_citation), parser)
            mixed_citation = mc.find('body/p/.') if mc.find('body/p/.') is not None else mc.find('body/.')

            mixed_citation.tag = 'mixed-citation'

            xml.append(utils.convert_all_html_tags_to_jats(mixed_citation))

            return data

    class ElementCitationPipe(plumber.Pipe):
        def transform(self, data):
            raw, xml = data

            translate_ptype = {
                'article': 'journal',
                'link': 'webpage',
                'conference': 'confproc',
                'undefined': 'other',
            }

            elementcitation = ET.Element('element-citation')
            elementcitation.set(
                'publication-type',
                translate_ptype.get(raw.publication_type, raw.publication_type)
            )

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

    class CommentPipe(plumber.Pipe):
        def precond(data):
            raw, xml = data

            if not raw.comment:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            comment = ET.Element('comment')

            comment.text = XLINK_REGEX.sub('xlink:href', raw.comment)

            if raw.publication_type == 'link' and raw.link:
                comment.text = 'Available at:'
                link = ET.Element('ext-link')
                link.set('ext-link-type', 'uri')
                link.set('{http://www.w3.org/1999/xlink}href', 'http://%s' % raw.link)
                link.text = 'link'
                comment.append(link)

            xml.find('./element-citation').append(comment)

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

            if not raw.authors:
                raise plumber.UnmetPrecondition()

        @plumber.precondition(precond)
        def transform(self, data):
            raw, xml = data

            persongroup = ET.Element('person-group')
            persongroup.set('person-group-type', 'author')
            if raw.authors:
                for author in raw.authors:
                    name = ET.Element('name')

                    if "surname" in author:
                        surname = ET.Element('surname')
                        surname.text = author['surname']
                        name.append(surname)

                    if "given_names" in author:
                        givennames = ET.Element('given-names')
                        givennames.text = author['given_names']
                        name.append(givennames)                

                    persongroup.append(name)

            xml.find('./element-citation').append(persongroup)

            return data

    def deploy(self, raw):

        transformed_data = self._ppl.run(raw, rewrap=True)

        return next(transformed_data)


class SetupArticlePipe(plumber.Pipe):

    def transform(self, data):

        nsmap = {
            'xml': 'http://www.w3.org/XML/1998/namespace',
            'xlink': 'http://www.w3.org/1999/xlink'
        }

        xml = ET.Element('article', nsmap=nsmap)
        xml.set('specific-use', 'sps-1.4')
        xml.set('dtd-version', '1.0')

        return data, xml


class XMLArticlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        translate_document_type = {
            u'news': 'rapid-communication',
            u'addendum': 'other',
            u'press-release': 'in-brief',
            u'undefined': 'other',
            u'abstract': 'other'
        }

        xml.set('{http://www.w3.org/XML/1998/namespace}lang', raw.original_language())
        xml.set('article-type', translate_document_type.get(raw.document_type, raw.document_type))

        return data


class XMLFrontPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        xml.append(ET.Element('front'))

        front = xml.find('front')
        front.append(ET.Element('journal-meta'))
        front.append(ET.Element('article-meta'))

        return data


class XMLBodyPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.original_html():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        body = ET.Element('body')
        p = ET.Element('p')
        p.text = raw.original_html()
        body.set('specific-use', 'quirks-mode')
        body.append(p)
        xml.append(body)

        return data


class XMLSubArticlePipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.translated_htmls():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for language, body in raw.translated_htmls().items():
            if language == raw.original_language():
                continue
            subarticle = ET.Element('sub-article')
            frontstub = ET.Element('front-stub')

            # ARTICLE CATEGORY
            if raw.section:
                articlecategories = ET.Element('article-categories')
                for lang, text in raw.translated_section().items():
                    if lang != language:
                        continue
                    subjectgroup = ET.Element('subj-group')
                    subjectgroup.set('subj-group-type', 'heading')
                    sbj = ET.Element('subject')
                    sbj.text = text
                    subjectgroup.append(sbj)    
                    articlecategories.append(subjectgroup)
                frontstub.append(articlecategories)

            # ARTICLE TITLE
            if raw.translated_titles():
                titlegroup = ET.Element('title-group')
                for lang, text in raw.translated_titles().items():
                    if lang != language:
                        continue
                    articletitle = ET.Element('article-title')
                    articletitle.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
                    articletitle.text = text
                    titlegroup.append(articletitle)
                frontstub.append(titlegroup)

            # ABSTRACT
            if raw.translated_abstracts():
                for lang, text in raw.translated_abstracts().items():
                    if lang != language:
                        continue
                    p = ET.Element('p')
                    p.text = text
                    abstract = ET.Element('abstract')
                    abstract.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
                    abstract.append(p)
                frontstub.append(abstract)

            # KEYWORDS
            if raw.keywords():
                for lang, keywords in raw.keywords().items():
                    if lang != language:
                        continue
                    kwd_group = ET.Element('kwd-group')
                    kwd_group.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
                    for keyword in keywords:
                        kwd = ET.Element('kwd')
                        kwd.text = keyword
                        kwd_group.append(kwd)
                    frontstub.append(kwd_group)

            subarticle.append(frontstub)
            subarticle.set('article-type', 'translation')
            subarticle.set('id', 'TR%s' % language)
            subarticle.set('{http://www.w3.org/XML/1998/namespace}lang', language)
            subarticle_body = ET.Element('body')
            subarticle_body.set('specific-use', 'quirks-mode')
            p = ET.Element('p')
            p.text = body
            subarticle_body.append(p)
            subarticle.append(subarticle_body)
            xml.append(subarticle)

        return data


class XMLJournalMetaJournalIdPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        journal_meta = xml.find('./front/journal-meta')

        journalid = ET.Element('journal-id')
        journalid.text = raw.journal.acronym
        journalid.set('journal-id-type', 'publisher-id')

        journal_meta.append(journalid)

        return data


class XMLJournalMetaJournalTitleGroupPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        journaltitle = ET.Element('journal-title')
        journaltitle.text = raw.journal.title

        journalabbrevtitle = ET.Element('abbrev-journal-title')
        journalabbrevtitle.text = raw.journal.abbreviated_title
        journalabbrevtitle.set('abbrev-type', 'publisher')

        journaltitlegroup = ET.Element('journal-title-group')
        journaltitlegroup.append(journaltitle)
        journaltitlegroup.append(journalabbrevtitle)

        xml.find('./front/journal-meta').append(journaltitlegroup)

        return data


class XMLJournalMetaISSNPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        if raw.journal.print_issn:
            pissn = ET.Element('issn')
            pissn.text = raw.journal.print_issn
            pissn.set('pub-type', 'ppub')
            xml.find('./front/journal-meta').append(pissn)

        if raw.journal.electronic_issn:
            eissn = ET.Element('issn')
            eissn.text = raw.journal.electronic_issn
            eissn.set('pub-type', 'epub')
            xml.find('./front/journal-meta').append(eissn)

        return data


class XMLJournalMetaPublisherPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        publisher = ET.Element('publisher')

        publishername = ET.Element('publisher-name')
        publishername.text = u'; '.join(raw.journal.publisher_name or [])
        publisher.append(publishername)

        if raw.journal.publisher_country:
            countrycode, countryname = raw.journal.publisher_country
            publishercountry = countryname or countrycode

        publisherloc = [
            raw.journal.publisher_city or u'',
            raw.journal.publisher_state or u'',
            publishercountry
        ]

        if raw.journal.publisher_country:
            publishercountry = ET.Element('publisher-loc')
            publishercountry.text = ', '.join(publisherloc)
            publisher.append(publishercountry)

        xml.find('./front/journal-meta').append(publisher)

        return data


class XMLArticleMetaHistoryPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        history = ET.Element('history')

        dates = {
         'received': raw.receive_date,
         'accepted': raw.acceptance_date,
         'rev-recd': raw.review_date,
        }

        for hist_type, hist_date in dates.items():
            if hist_date:
                year = hist_date[0:4]
                month = hist_date[5:7]
                day = hist_date[8:10]

                hdate = ET.Element('date')
                hdate.set('date-type', hist_type)
                if day:
                    hdate_day = ET.Element('day')
                    hdate_day.text = day
                    hdate.append(hdate_day)
                if month:
                    hdate_month = ET.Element('month')
                    hdate_month.text = month
                    hdate.append(hdate_month)
                if year:
                    hdate_year = ET.Element('year')
                    hdate_year.text = year
                    hdate.append(hdate_year)
                history.append(hdate)

        if len(history.findall('date')) > 0:
            xml.find('./front/article-meta').append(history)

        return data


class XMLArticleMetaArticleIdPublisherPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        article_meta = xml.find('./front/article-meta')

        try:
            if raw.is_ahead_of_print:
                otherid = ET.Element('article-id')
                otherid.text = raw.order
                otherid.set('pub-id-type', 'other')
                article_meta.append(otherid)
        except UnavailableMetadataException as e:
            pass

        articleidpublisher = ET.Element('article-id')
        articleidpublisher.set('pub-id-type', 'publisher-id')
        articleidpublisher.text = raw.publisher_id

        article_meta.append(articleidpublisher)

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

        xml.find('./front/article-meta').append(articleiddoi)

        return data


class XMLArticleMetaArticleCategoriesPipe(plumber.Pipe):
    def precond(data):

        raw, xml = data

        if not raw.original_section():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        subjectgroup = ET.Element('subj-group')
        subjectgroup.set('subj-group-type', 'heading')

        sbj = ET.Element('subject')
        sbj.text = raw.original_section()

        subjectgroup.append(sbj)

        articlecategories = ET.Element('article-categories')
        articlecategories.append(subjectgroup)

        xml.find('./front/article-meta').append(articlecategories)

        return data


class XMLArticleMetaTitleGroupPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        articletitle = ET.Element('article-title')

        articletitle.text = raw.original_title()

        titlegroup = ET.Element('title-group')
        titlegroup.append(articletitle)

        xml.find('./front/article-meta').append(titlegroup)

        return data


class XMLArticleMetaTranslatedTitleGroupPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.translated_titles():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        html_fulltext_langs = []
        if raw.translated_htmls():
            html_fulltext_langs = [i for i in raw.translated_htmls().keys()]

        for lang, title in raw.translated_titles().items():

            if lang in html_fulltext_langs:
                continue

            transtitle = ET.Element('trans-title')
            transtitle.text = title

            transtitlegrp = ET.Element('trans-title-group')
            transtitlegrp.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
            transtitlegrp.append(transtitle)

            xml.find('./front/article-meta/title-group').append(transtitlegrp)

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

                ndx = AFF_REGEX_JUST_NUMBERS.findall(xr)

                if len(ndx) == 0:
                    ndx = xr
                else:
                    ndx = 'aff%s' % ndx[0]

                xref.set('rid', ndx)
                contrib.append(xref)

            contribgroup.append(contrib)

        xml.find('./front/article-meta').append(contribgroup)

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

            ndx = AFF_REGEX_JUST_NUMBERS.findall(affiliation['index'])

            if len(ndx) == 0:
                ndx = affiliation['index']
            else:
                ndx = 'aff%s' % ndx[0]

            aff.set('id', ndx)

            if 'city' in affiliation or 'state' in affiliation:
                addrline = ET.Element('addr-line')
                if 'city' in affiliation:
                    city = ET.Element('named-content')
                    city.set('content-type', 'city')
                    city.text = affiliation['city']
                    addrline.append(city)
                if 'state' in affiliation:
                    state = ET.Element('named-content')
                    state.set('content-type', 'state')
                    state.text = affiliation['state']
                    addrline.append(state)
                aff.append(addrline)

            if 'institution' in affiliation:
                institution = ET.Element('institution')
                institution.text = affiliation['institution']
                institution.set('content-type', 'orgname')
                aff.append(institution)

            if 'orgdiv1' in affiliation or 'division' in affiliation:
                institution = ET.Element('institution')
                institution.text = ' '.join([affiliation.get('orgdiv1', ''), affiliation.get('division', '')])
                institution.set('content-type', 'orgdiv1')
                aff.append(institution)

            if 'orgdiv2' in affiliation:
                institution = ET.Element('institution')
                institution.text = affiliation['orgdiv2']
                institution.set('content-type', 'orgdiv2')
                aff.append(institution)

            if 'country' in affiliation:
                country = ET.Element('country')
                country.text = affiliation['country']
                if 'country_iso_3166' in affiliation:
                    country.set('country', affiliation['country_iso_3166'])
                aff.append(country)

            if 'email' in affiliation:
                email = ET.Element('email')
                email.text = affiliation['email']
                aff.append(email)


            xml.find('./front/article-meta').append(aff)

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
        pubdate.set('pub-type', 'epub-ppub')

        year = ET.Element('year')
        year.text = raw.publication_date[0:4]

        if raw.publication_date[5:7]:
            month = ET.Element('month')
            month.text = raw.publication_date[5:7]
            pubdate.append(month)

        pubdate.append(year)

        articlemeta = xml.find('./front/article-meta')
        articlemeta.append(pubdate)

        return data


class XMLArticleMetaPagesInfoPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        fpage = ET.Element('fpage')
        fpage.text = raw.start_page

        lpage = ET.Element('lpage')
        lpage.text = raw.end_page

        articlemeta = xml.find('./front/article-meta')

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

        articlemeta = xml.find('./front/article-meta')
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

        label_volume = raw.issue.volume or ''
        label_issue = raw.issue.number.replace('ahead', '') if raw.issue.number else ''

        label_suppl_issue = ' suppl %s' % raw.issue.supplement_number if raw.issue.supplement_number else ''

        if label_suppl_issue:
            label_issue += label_suppl_issue

        label_suppl_volume = ' suppl %s' % raw.issue.supplement_volume if raw.issue.supplement_volume else ''

        if label_suppl_volume:
            label_issue += label_suppl_volume

        label_issue = SUPPLBEG_REGEX.sub('', label_issue)
        label_issue = SUPPLEND_REGEX.sub('', label_issue)

        articlemeta = xml.find('./front/article-meta')

        if label_volume:
            vol = ET.Element('volume')
            vol.text = label_volume.strip()
            articlemeta.append(vol)

        if label_issue:
            issue = ET.Element('issue')
            issue.text = label_issue.strip()
            articlemeta.append(issue)

        return data


class XMLArticleMetaAbstractsPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        p = ET.Element('p')
        p.text = raw.original_abstract()

        abstract = ET.Element('abstract')
        abstract.append(p)

        articlemeta = xml.find('./front/article-meta')

        if raw.original_abstract():
            articlemeta.append(abstract)

        if raw.translated_abstracts():

            html_fulltext_langs = []
            if raw.translated_htmls():
                html_fulltext_langs = [i for i in raw.translated_htmls().keys()]

            for lang, text in raw.translated_abstracts().items():

                if lang in html_fulltext_langs:
                    continue

                p = ET.Element('p')
                p.text = text

                abstract = ET.Element('trans-abstract')
                abstract.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
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

        articlemeta = xml.find('./front/article-meta')

        for lang, keywords in raw.keywords().items():

            html_fulltext_langs = []
            if raw.translated_htmls():
                html_fulltext_langs = [i for i in raw.translated_htmls().keys()]

            if lang in html_fulltext_langs:
                continue

            kwdgroup = ET.Element('kwd-group')
            kwdgroup.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
            kwdgroup.set('kwd-group-type', 'author-generated')
            for keyword in keywords:
                kwd = ET.Element('kwd')
                kwd.text = keyword
                kwdgroup.append(kwd)
            articlemeta.append(kwdgroup)

        return data

class XMLArticleMetaCountsPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        articlemeta = xml.find('./front/article-meta')

        counts = ET.Element('counts')

        count_refs = ET.Element('ref-count')
        if raw.citations:
            count_refs.set('count', str(len(raw.citations)))
        else:
            count_refs.set('count', '0')

        try:
            startpage = int(raw.start_page)
        except (ValueError, TypeError):
            startpage = None

        try:
            endpage = int(raw.end_page)
        except (ValueError, TypeError):
            endpage = None

        pages = 0
        if startpage != None and endpage != None:
            pages = (endpage - startpage) + 1
            if pages < 0:
                pages = 0

        count_pages = ET.Element('page-count')
        count_pages.set('count', str(pages))

        # Esses elementos possuem contagem 0 pois o legado não identifica esses elementos
        count_fig = ET.Element('fig-count')
        count_fig.set('count', '0')
        count_table = ET.Element('table-count')
        count_table.set('count', '0')
        count_equation = ET.Element('equation-count')
        count_equation.set('count', '0')

        counts.append(count_fig)
        counts.append(count_table)
        counts.append(count_equation)

        counts.append(count_refs)
        counts.append(count_pages)

        articlemeta.append(counts)

        return data


class XMLArticleMetaPermissionPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.permissions:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        articlemeta = xml.find('./front/article-meta')

        permissions = ET.Element('permissions')
        dlicense = ET.Element('license')
        dlicense.set('license-type', 'open-access')
        dlicense.set('{http://www.w3.org/1999/xlink}href', raw.permissions['url'])
        dlicense.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')

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

        article = xml.find('.')
        article.append(ET.Element('back'))

        back = article.find('back')
        back.append(ET.Element('ref-list'))

        reflist = xml.find('./back/ref-list')

        cit = XMLCitation()
        for citation in raw.citations:
            reflist.append(cit.deploy(citation)[1])

        return data


class XMLClosePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        data = ET.tostring(xml, encoding="utf-8", method="xml", doctype='<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">')

        return data
