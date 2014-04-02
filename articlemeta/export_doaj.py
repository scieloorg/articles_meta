#conding: utf-8
import xml.etree.ElementTree as ET

import plumber


class SetupArticlePipe(plumber.Pipe):

    def transform(self, data):

        xml = ET.Element('records')

        return data, xml


class XMLArticlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        article = ET.Element('record')

        xml.append(article)

        return data


class XMLJournalMetaJournalTitlePipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        journaltitle = ET.Element('journalTitle')
        journaltitle.text = raw.journal_title

        xml.find('./record').append(journaltitle)

        return data


class XMLJournalMetaISSNPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        issn = ET.Element('issn')
        issn.text = raw.any_issn()

        xml.find('./record').append(issn)

        return data


class XMLJournalMetaPublisherPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        publisher = ET.Element('publisher')
        publisher.text = raw.publisher_name

        xml.find('./record').append(publisher)

        return data


class XMLArticleMetaIdPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        uniquearticleid = ET.Element('publisherId')
        uniquearticleid.text = raw.publisher_id

        xml.find('./record').append(uniquearticleid)

        return data


class XMLArticleMetaArticleIdDOIPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.doi:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        articleiddoi = ET.Element('doi')
        articleiddoi.text = raw.doi

        xml.find('./record').append(articleiddoi)

        return data


class XMLArticleMetaTitlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        title = ET.Element('title')
        title.text = raw.original_title()

        xml.find('./record').append(title)

        return data


class XMLArticleMetaAuthorsPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.authors:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        contribgroup = ET.Element('authors')

        for author in raw.authors:
            names = [author.get('given_names', ''), author.get('surname', '')]
            contribname = ET.Element('name')
            contribname.text = ' '.join(names)

            contrib = ET.Element('author')
            contrib.append(contribname)

            for xr in author.get('xref', []):
                xref = ET.Element('affiliationId')
                xref.text = xr
                contrib.append(xref)

            contribgroup.append(contrib)

        xml.find('./record').append(contribgroup)

        return data


class XMLArticleMetaAffiliationPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data

        if not raw.affiliations:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        affs = ET.Element('affiliationsList')

        for affiliation in raw.affiliations:

            if 'institution' in affiliation:
                aff = ET.Element('affiliationName')
                aff.set('affiliationId', affiliation['index'])
                aff.text = affiliation['institution']
                affs.append(aff)

        xml.find('./record').append(affs)

        return data


class XMLArticleMetaPublicationDatePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        pubdate = ET.Element('publicationDate')
        pubdate.text = raw.publication_date

        xml.find('./record').append(pubdate)

        return data


class XMLArticleMetaStartPagePipe(plumber.Pipe):

    def precond(data):

        raw, xml = data
        if not raw.start_page:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        startpage = ET.Element('startPage')
        startpage.text = raw.start_page

        xml.find('./record').append(startpage)

        return data


class XMLArticleMetaEndPagePipe(plumber.Pipe):

    def precond(data):

        raw, xml = data
        if not raw.end_page:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        endpage = ET.Element('endPage')
        endpage.text = raw.end_page

        xml.find('./record').append(endpage)

        return data


class XMLArticleMetaVolumePipe(plumber.Pipe):

    def precond(data):

        raw, xml = data
        if not raw.volume:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        volume = ET.Element('volume')
        volume.text = raw.volume

        xml.find('./record').append(volume)

        return data


class XMLArticleMetaIssuePipe(plumber.Pipe):

    def precond(data):

        raw, xml = data
        if not raw.issue:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        issue = ET.Element('issue')
        issue.text = raw.issue

        xml.find('./record').append(issue)

        return data


class XMLArticleMetaDocumentTypePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        documenttype = ET.Element('documentType')
        documenttype.text = raw.document_type

        xml.find('./record').append(documenttype)

        return data


class XMLArticleMetaFullTextUrlPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data
        if not raw.html_url:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        url = ET.Element('fullTextUrl')
        url.set('format', 'html')
        url.text = raw.html_url

        xml.find('./record').append(url)

        return data


class XMLArticleMetaAbstractsPipe(plumber.Pipe):

    def precond(data):

        raw, xml = data
        if not raw.original_abstract() and not raw.translated_abstracts():
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        articlemeta = xml.find('./record')

        if raw.original_abstract():
            abstract = ET.Element('abstract')
            abstract.set('language', raw.original_language())
            abstract.text = raw.original_abstract()
            articlemeta.append(abstract)

        if raw.translated_abstracts():
            for lang, text in raw.translated_abstracts().items():
                abstract = ET.Element('abstract')
                abstract.set('language', lang)
                abstract.text = text
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

        articlemeta = xml.find('./record')

        if raw.keywords():
            for lang, keywords in raw.keywords().items():
                kwdgroup = ET.Element('keywords')
                kwdgroup.set('language', lang)
                for keyword in keywords:
                    kwd = ET.Element('keyword')
                    kwd.text = keyword
                    kwdgroup.append(kwd)
                articlemeta.append(kwdgroup)

        return data


class XMLClosePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        data = ET.tostring(xml, encoding="utf-8", method="xml")

        return data
