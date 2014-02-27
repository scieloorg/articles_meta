# coding: utf-8
import unicodedata

from xylose.scielodocument import Article


def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if unicodedata.category(x)[0] == 'L').lower()


def gen_citations_title_keys(article):
    """
    This method is responsible to receive an array having the article titles
    available for the a given article and convert then into keys exemple.
    from: ['Health care after 60th', 'Cuidados de saúde após os sessenta anos']
    to: ['healthcareafter60th', 'cuidadosdesaudeaposossessentaanos']
    """

    def get_citation_titles():
        titles = []

        for citation in article.citations:
            title = ''
            if citation.article_title:
                title = citation.article_title
            elif citation.chapter_title:
                title = citation.chapter_title
            elif citation.thesis_title:
                title = citation.thesis_title
            elif citation.conference_title:
                title = citation.conference_title
            elif citation.link_title:
                title = citation.link_title

            if not title:
                continue

            titles.append(remove_accents(title))

        if len(titles) == 0:
            return None

        return titles

    def get_citation_titles_author_year():
        titles = []

        for citation in article.citations:

            if not citation.date:
                continue

            data = []
            title = ''
            if citation.article_title:
                title = citation.article_title
            elif citation.chapter_title:
                title = citation.chapter_title
            elif citation.thesis_title:
                title = citation.thesis_title
            elif citation.conference_title:
                title = citation.conference_title
            elif citation.link_title:
                title = citation.link_title

            if not title:
                continue

            data.append(title)

            author = ''
            if citation.authors:
                author = citation.authors[0].get('given_names', '')+citation.authors[0].get('surname', '')
            elif citation.monographic_authors:
                author = citation.monographic_authors[0].get('given_names', '')+citation.monographic_authors[0].get('surname', '')

            if not author:
                continue

            data.append(author)

            key = remove_accents(''.join(data))

            key += citation.date[0:4]

            if key:
                titles.append(key)

        if len(titles) == 0:
            return None

        return titles

    if not article.citations:
        return None

    no_accents_strings = get_citation_titles()
    no_accents_strings_author_year = get_citation_titles_author_year()

    if not no_accents_strings:
        return None

    title_keys = {}
    title_keys['citations_title_no_accents'] = no_accents_strings
    title_keys['citations_title_author_year_no_accents'] = no_accents_strings_author_year

    return title_keys


def gen_title_keys(article):
    """
    This method is responsible to receive an array having the article titles
    available for the a given article and convert then into keys exemple.
    from: ['Health care after 60th', 'Cuidados de saúde após os sessenta anos']
    to: ['healthcareafter60th', 'cuidadosdesaudeaposossessentaanos']
    """

    def titles():
        titles = []
        if article.original_title():
            titles.append(article.original_title())

        if article.translated_titles():
            for title in article.translated_titles().values():
                titles.append(title)

        if len(titles) == 0:
            return None

        return titles

    titles = titles()

    if not titles:
        return None

    no_accents_strings = []
    no_accents_strings_author_year = []
    for title in titles:
        ra = remove_accents(title)
        no_accents_strings.append(ra)

        if not article.authors:
            continue

        author = article.authors[0].get('given_names', '')+article.authors[0].get('surname', '')
        author = remove_accents(author)
        no_accents_strings_author_year.append(
            ra+author+article.publication_date[0:4])

    title_keys = {}
    title_keys['no_accents_strings'] = no_accents_strings
    title_keys['no_accents_strings_author_year'] = no_accents_strings_author_year

    return title_keys


class DataBroker(object):

    def __init__(self, databroker):
        self.db = databroker

    def _check_article_meta(self, metadata):
        """
            This method will check the given metadata and retrieve
            a new dictionary with some new fields.
        """

        article = Article(metadata)

        issns = set([article.any_issn(priority=u'electronic'),
                    article.any_issn(priority=u'print')])

        metadata['code_issue'] = article.publisher_id[1:18]
        metadata['code_title'] = list(issns)
        metadata['collection'] = article.collection_acronym
        metadata['publication_year'] = article.publication_date[0:4]
        metadata['validated_scielo'] = 'False'
        metadata['validated_wos'] = 'False'
        metadata['sent_wos'] = 'False'
        metadata['applicable'] = 'False'

        gtk = gen_title_keys(article)
        if gtk:
            metadata.update(gtk)

        gctk = gen_citations_title_keys(article)
        if gctk:
            metadata.update(gctk)

        return metadata

    def _check_journal_meta(self, metadata):
        """
            This method will check the given metadata and retrieve
            a new dictionary with some new fields.
        """
        journal = Article({'title': metadata, 'article': {}, 'citations': {}})

        issns = set([journal.any_issn(priority=u'electronic'),
                     journal.any_issn(priority=u'print')])

        metadata['code'] = list(issns)
        metadata['collection'] = journal.collection_acronym

        return metadata

    def journal(self, collection=None, issn=None):

        fltr = {}

        if collection:
            fltr['collection'] = collection

        if issn:
            fltr['code'] = issn

        data = self.db['journals'].find(fltr, {'_id': 0})

        if not data:
            return None

        return [i for i in data]

    def delete_journal(self, issn, collection=None):

        fltr = {
            'code': issn,
            'collection': collection
        }

        self.db['journals'].remove(fltr)

    def add_journal(self, metadata):

        journal = self._check_journal_meta(metadata)

        if not journal:
            return None

        collection = journal['v992'][0]['_']

        self.db['journals'].update(
            {'code': journal['code'], 'collection': collection},
            {'$set': journal},
            safe=False,
            upsert=True
        )

        return journal

    def collection(self):

        data = self.db['collections'].find({}, {'_id': 0})

        if not data:
            return None

        return [i for i in data]

    def identifiers_journal(self, collection=None, limit=1000, offset=0):

        fltr = {}
        if collection:
            fltr['collection'] = collection

        total = self.db['journals'].find(fltr).count()
        data = self.db['journals'].find(fltr, {'code': 1, 'collection': 1}).skip(offset).limit(limit)

        meta = {'limit': limit,
                'offset': offset,
                'filter': fltr,
                'total': total}

        result = {'meta': meta, 'objects': [{'code': i['code'], 'collection': i['collection']} for i in data]}

        return result

    def identifiers_article(self, collection=None, issn=None, limit=1000, offset=0):

        fltr = {}
        if collection:
            fltr['collection'] = collection
        if issn:
            fltr['code_title'] = issn

        total = self.db['articles'].find(fltr).count()
        data = self.db['articles'].find(fltr, {'code': 1, 'collection': 1}).skip(offset).limit(limit)
        meta = {'limit': limit,
                'offset': offset,
                'filter': fltr,
                'total': total}

        result = {'meta': meta, 'objects': [{'code': i['code'], 'collection': i['collection']} for i in data]}

        return result

    def get_article(self, code, collection=None):

        fltr = {'code': code}
        if collection:
            fltr['collection'] = collection        

        data = self.db['articles'].find_one(fltr)

        if not data:
            return None

        del(data['_id'])

        return data

    def exists_article(self, code, collection=None):
        
        fltr = {'code': code}
        if collection:
            fltr['collection'] = collection    

        if self.db['articles'].find(fltr).count() >= 1:
            return True

        return False

    def delete_article(self, code, collection=None):

        fltr = {
            'code': code,
            'collection': collection
        }

        self.db['articles'].remove(fltr)

    def add_article(self, metadata):

        article = self._check_article_meta(metadata)

        if not article:
            return None

        code = article['article']['v880'][0]['_']
        collection = article['article']['v992'][0]['_']

        self.db['articles'].update(
            {'code': code, 'collection': collection},
            {'$set': article},
            safe=False,
            upsert=True
        )

        return article
