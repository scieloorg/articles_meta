#conding: utf-8
from xylose.scielodocument import Article
import xml.etree.ElementTree as ET
import plumber


class SetupPipe(plumber.Pipe):

    def transform(self, data):

        xml = ET.Element('articles')
        xml.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        xml.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        xml.set('xsi:noNamespaceSchemaLocation', 'ThomsonReuters_publishing_1.06.xsd')
        xml.set('dtd-version', '1.06')

        return data, xml


class XMLArticlePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        article_types = {
            'rc': 'undefined',
            'ab': 'abstract',
            'pv': 'article-commentary',
            'ed': 'editorial',
            'in': 'oration',
            'tr': 'research-article',
            'up': 'review-article',
            'oa': 'research-article',
            'an': 'undefined',
            'ax': 'undefined',
            'mt': 'research-article',
            'le': 'letter',
            'ra': 'review-article',
            'nd': 'undefined',
            'cr': 'case-report',
            'sc': 'rapid-communication',
            'co': 'article-commentary',
            'rn': 'brief-report'}

        article = ET.Element('article')
        article.set('lang_id', raw.original_language())
        article.set('article-type', raw.document_type)

        xml.append(article)

        return data


class XMLFrontBackPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        article = xml.find('article')
        article.append(ET.Element('front'))
        article.append(ET.Element('back'))

        front = article.find('front')
        front.append(ET.Element('journal-meta'))
        front.append(ET.Element('article-meta'))

        back = article.find('back')
        back.append(ET.Element('ref-list'))

        return data


class XMLJournalMetaJournalIdPipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        journalid = ET.Element('journal-id')
        journalid.text = raw.journal_acronym
        journalid.set('journal-id-type', 'publisher')

        xml.find('./article/front/journal-meta').append(journalid)

        return data


class XMLJournalMetaJournalTitleGroupPipe(plumber.Pipe):
    def transform(self, data):
        raw, xml = data

        journaltitle = ET.Element('journal-title')
        journaltitle.text = raw.journal_title

        journalabbrevtitle = ET.Element('abbrev-journal-title')
        journalabbrevtitle.text = raw.journal_abbreviated_title

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

        if not raw.wos_subject_areas:
            raise plumber.UnmetPrecondition()

    @plumber.precondition(precond)
    def transform(self, data):
        raw, xml = data

        subjectgroup = ET.Element('subj-group')

        for subject in raw.wos_subject_areas:
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

        articletitle = ET.Element('article-title')
        articletitle.set('lang_id', raw.original_language())

        articletitle.text = raw.original_title()

        titlegroup = ET.Element('title-group')
        titlegroup.append(articletitle)

        xml.find('./article/front/article-meta').append(titlegroup)

        return data


class XMLClosePipe(plumber.Pipe):

    def transform(self, data):
        raw, xml = data

        data = ET.tostring(xml, encoding="utf-8", method="xml")

        return data


class Export(object):

    def __init__(self, article):
        self._article = Article(article)

    def xmlwos(self):

        ppl = plumber.Pipeline(SetupPipe(),
                               XMLArticlePipe(),
                               XMLFrontBackPipe(),
                               XMLJournalMetaJournalIdPipe(),
                               XMLJournalMetaJournalTitleGroupPipe(),
                               XMLJournalMetaISSNPipe(),
                               XMLJournalMetaPublisherPipe(),
                               XMLArticleMetaUniqueArticleIdPipe(),
                               XMLArticleMetaArticleIdPublisherPipe(),
                               XMLArticleMetaArticleIdDOIPipe(),
                               XMLArticleMetaArticleCategoriesPipe(),
                               XMLClosePipe())

        transformed_data = ppl.run(self._article, rewrap=True)

        return next(transformed_data)
