#coding: utf-8
from lxml import etree as ET

import plumber


class XMLCitation(object):

    def __init__(self):
        self._ppl = plumber.Pipeline(self.SetupCitationPipe(),
                                     self.RefIdPipe(),
                                     self.ElementCitationPipe(),
                                     self.ArticleTitlePipe(),
                                     self.SourcePipe(),
                                     self.DatePipe(),
                                     self.StartPagePipe(),
                                     self.EndPagePipe(),
                                     self.IssuePipe(),
                                     self.VolumePipe(),
                                     self.PersonGroupPipe())

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

            translate_ptype = {
                'article': 'journal',
                'link': 'webpage'
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

            if not raw.authors and not raw.monographic_authors:
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

            if raw.monographic_authors:
                for author in raw.monographic_authors:
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
        xml.set('specific-use', 'sps-1.1')
        xml.set('dtd-version', '1.0')

        return data, xml


class XMLArticlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        xml.set('{http://www.w3.org/XML/1998/namespace}lang', raw.original_language())
        xml.set('article-type', raw.document_type)

        return data


class XMLFrontPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        xml.append(ET.Element('front'))

        front = xml.find('front')
        front.append(ET.Element('journal-meta'))
        front.append(ET.Element('article-meta'))

        return data


class XMLJournalMetaJournalIdPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        journalid = ET.Element('journal-id')
        journalid.text = raw.journal_acronym
        journalid.set('journal-id-type', 'publisher-id')

        xml.find('./front/journal-meta').append(journalid)

        return data


class XMLJournalMetaJournalTitleGroupPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        journaltitle = ET.Element('journal-title')
        journaltitle.text = raw.journal_title

        journalabbrevtitle = ET.Element('abbrev-journal-title')
        journalabbrevtitle.text = raw.journal_abbreviated_title
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

        publishername = ET.Element('publisher-name')
        publishername.text = raw.publisher_name

        publisherloc = ET.Element('publisher-loc')
        publisherloc.text = raw.publisher_loc

        publisher = ET.Element('publisher')
        publisher.append(publishername)
        publisher.append(publisherloc)

        xml.find('./front/journal-meta').append(publisher)

        return data


class XMLArticleMetaArticleIdPublisherPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        articleidpublisher = ET.Element('article-id')
        articleidpublisher.set('pub-id-type', 'publisher-id')
        articleidpublisher.text = raw.publisher_id

        xml.find('./front/article-meta').append(articleidpublisher)

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

        if not raw.wos_subject_areas:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        subjectgroup = ET.Element('subj-group')
        subjectgroup.set('subj-group-type', 'heading')

        for subject in raw.wos_subject_areas:
            sbj = ET.Element('subject')
            sbj.text = subject

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

        for lang, title in raw.translated_titles().items():
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
                xref.set('rid', 'aff%s' % xr.upper().replace('A', ''))
                contrib.append(xref)

            contribgroup.append(contrib)

        xml.find('./front/article-meta').append(contribgroup)

        return data


class XMLArticleMetaAffiliationPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.affiliations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        for affiliation in raw.affiliations:

            aff = ET.Element('aff')
            aff.set('id', 'aff%s' % affiliation['index'].upper().replace('A',''))

            if 'addr_line' in affiliation:
                addrline = ET.Element('addr-line')
                addrline.text = affiliation['addr_line']
                aff.append(addrline)

            if 'institution' in affiliation:
                institution = ET.Element('institution')
                institution.text = affiliation['institution']
                institution.set('content-type', 'original')
                aff.append(institution)

            if 'country' in affiliation:
                country = ET.Element('country')
                country.text = affiliation['country']
                aff.append(country)

            xml.find('./front/article-meta').append(aff)

        return data


class XMLArticleMetaGeneralInfoPipe(plumber.Pipe):

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

        fpage = ET.Element('fpage')
        fpage.text = raw.start_page

        lpage = ET.Element('lpage')
        lpage.text = raw.end_page

        vol = ET.Element('volume')
        vol.text = raw.volume

        issue = ET.Element('issue')
        issue.text = raw.issue

        articlemeta = xml.find('./front/article-meta')
        articlemeta.append(pubdate)
        if raw.volume:
            articlemeta.append(vol)
        if raw.issue:
            articlemeta.append(issue)
        if raw.start_page:
            articlemeta.append(fpage)
        if raw.end_page:
            articlemeta.append(lpage)

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
            for lang, text in raw.translated_abstracts().items():
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
        count_refs.set('count', str(len(raw.citations)))

        try:
            startpage = int(raw.start_page)
        except:
            startpage = 0


        try:
            endpage = int(raw.end_page)
        except:
            endpage = 0

        pages = endpage - startpage
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
