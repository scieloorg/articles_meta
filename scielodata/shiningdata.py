class ShineData(object):

    def __init__(self, response, doi_prefix, article_types):
        self.data = response
        self.article_types = article_types

        if doi_prefix:
            self.doi_prefix = doi_prefix

    @property
    def article(self):
        article = {}
        article['original_language'] = self.data['article']['v40'][0]['_']
        article['journal-id'] = self.data['title']['v930'][0]['_'].lower()
        article['issn'] = self.data['title']['v400'][0]['_'].upper()
        article['article-id'] = self.data['article']['v880'][0]['_'].upper()

        # Defining Article type according to dict defined into choices.py
        if 'v71' in self.data['article']:
            article_type_code = self.data['article']['v71'][0]['_']
            if article_type_code in self.article_types:
                article['article_type'] = self.article_types[article_type_code]
            else:
                article['article_type'] = self.article_types['nd']
        else:
            article['article_type'] = self.article_types['nd']

        if 'v690' in self.data['title']:
            article['scielo-url'] = self.data['title']['v690'][0]['_']
        elif 'v69' in self.data['article']:
            article['scielo-url'] = self.data['article']['v69'][0]['_']

        if 'doi' in self.data['article']:
            article['article-id-doi'] = self.data['article']['doi']

        if 'v100' in self.data['title']:
            article['journal-title'] = self.data['title']['v100'][0]['_']

        if 'v110' in self.data['title']:
            article['journal-subtitle'] = self.data['title']['v110'][0]['_']

        if 'v150' in self.data['title']:
            article['abbrev-journal-title'] = self.data['title']['v150'][0]['_']

        if 'v480' in self.data['title']:
            article['publisher-name'] = self.data['title']['v480'][0]['_']

        if 'v490' in self.data['title']:
            article['publisher-loc'] = self.data['title']['v490'][0]['_']

        if 'v31' in self.data['article']:
            article['volume'] = self.data['article']['v31'][0]['_']

        if 'v32' in self.data['article']:
            article['issue'] = self.data['article']['v32'][0]['_']

        # Supplement
        if 'v131' in self.data['article'] or 'v132' in self.data['article']:
            supplv = u' '
            suppln = u' '
            if 'v131' in self.data['article']:
                supplv = u"v. " + self.data['article']['v131'][0]['_']
            if 'v132' in self.data['article']:
                suppln = u"n. " + self.data['article']['v132'][0]['_']

            article['supplement'] = "Suppl. {0} {1}".format(supplv, suppln)

        # Pages
        if 'v14' in self.data['article']:
            if 'f' in self.data['article']['v14'][0]:
                article['fpage'] = self.data['article']['v14'][0]['f']
            if 'l' in self.data['article']['v14'][0]:
                article['lpage'] = self.data['article']['v14'][0]['l']

        # Article titles
        article['group-title'] = {}
        article['group-title']['article-title'] = {}
        if 'v12' in self.data['article']:
            article['group-title']['trans-title'] = {}
            for title in self.data['article']['v12']:
                if 'l' in title:
                    if title['l'] == article['original_language']:
                        article['group-title']['article-title'].setdefault(title['l'],
                            title['_']
                            )
                    else:
                        article['group-title']['trans-title'].setdefault(title['l'],
                            title['_']
                            )
        else:
            article['group-title']['article-title'] = {'zz': 'Not Available'}

        # Authors
        if 'v10' in self.data['article']:
            article['contrib-group'] = []
            for author in self.data['article']['v10']:
                authordict = {}
                if 's' in author:
                    authordict['surname'] = author['s']
                if 'n' in author:
                    authordict['given-names'] = author['n']
                if 'r' in author:
                    authordict['role'] = author['r']
                if '1' in author:
                    authordict['xref'] = author['1']

                article['contrib-group'].append(authordict)

        # Affiliations
        if 'v70' in self.data['article']:
            article['aff-group'] = []
            for affiliation in self.data['article']['v70']:
                affdict = {}
                if '_' in affiliation:
                    if len(affiliation['_'].strip()) > 0:
                        affdict['institution'] = affiliation['_']
                        if 'i' in affiliation:
                            affdict['index'] = affiliation['i']
                        else:
                            affdict['index'] = 'nd'
                        if 'c' in affiliation:
                            affdict['addr-line'] = affiliation['c']
                        if 'p' in affiliation:
                            affdict['country'] = affiliation['p']
                        if 'e' in affiliation:
                            affdict['email'] = affiliation['e']
                        article['aff-group'].append(affdict)

        # Publication date
        article['pub-date'] = {}
        if self.data['article']['v65'][0]['_'][6:8] != '00':
            article['pub-date']['day'] = self.data['article']['v65'][0]['_'][6:8]
        if self.data['article']['v65'][0]['_'][4:6] != '00':
            article['pub-date']['month'] = self.data['article']['v65'][0]['_'][4:6]
        article['pub-date']['year'] = self.data['article']['v65'][0]['_'][0:4]

        # Url
        if 'scielo-url' in article:
            article['self-uri'] = {}
            article['self-uri']['full-text-page'] = "http://{0}/scielo.php?script=sci_arttext&pid={1}&lng=en&tlng=en".format(article['scielo-url'].replace('http://', ''), article['article-id'])
            article['self-uri']['issue-page'] = "http://{0}/scielo.php?script=sci_issuetoc&pid={1}&lng=en&tlng=en".format(article['scielo-url'].replace('http://', ''), article['article-id'][0:18])
            article['self-uri']['journal-page'] = "http://{0}/scielo.php?script=sci_serial&pid={1}&lng=en&tlng=en".format(article['scielo-url'].replace('http://', ''), article['article-id'][1:10])

        # Abstract
        if 'v83' in self.data['article']:
            article['group-abstract'] = {}
            article['group-abstract']['abstract'] = {}
            article['group-abstract']['trans-abstract'] = {}
            for abstract in self.data['article']['v83']:
                if 'a' in abstract and 'l' in abstract:  # Validating this, because some original 'isis' records doesn't have the abstract driving the tool to an unexpected error: ex. S0066-782X2012001300004
                    if abstract['l'] == article['original_language']:
                        article['group-abstract']['abstract'].setdefault(
                            abstract['l'],
                            abstract['a']
                            )
                    else:
                        article['group-abstract']['trans-abstract'].setdefault(
                            abstract['l'],
                            abstract['a']
                            )

        # Keyword
        if 'v85' in self.data['article']:
            article['kwd-group'] = {}
            for keyword in self.data['article']['v85']:
                if 'k' in keyword and 'l' in keyword:
                    group = article['kwd-group'].setdefault(keyword['l'], [])
                    group.append(keyword['k'])

        # Journal WoS Subjects
        if 'v854' in self.data['title']:
            article['journal-subjects'] = []
            for subject in self.data['title']['v854']:
                if '_' in subject:
                    article['journal-subjects'].append(subject['_'])
                else:
                    article['journal-subjects'].append(subject)

        return article

    @property
    def citations(self):
        citations = []
        for data in self.data['citations']:
            citation = {}

            if 'v701' in data:
                citation['order'] = data['v701'][0]['_']

            # Citation type [book, article]
            if 'v18' in data:
                citation['publication-type'] = 'book'
            elif 'v12' in data:
                citation['publication-type'] = 'article'
            elif 'v53' in data:
                citation['publication-type'] = 'conference'
            elif 'v45' in data:
                citation['publication-type'] = 'thesis'
            else:
                citation['publication-type'] = 'nd'

            # Journal Title instead of Book title in source element.
            if 'v30' in data:
                citation['source'] = data['v30'][0]['_']

            # Citation title
            if citation['publication-type'] == 'book':
                citation['source'] = data['v18'][0]['_']
                if 'v12' in data:
                    citation['chapter-title'] = data['v12'][0]['_']
            elif citation['publication-type'] == 'article':
                citation['article-title'] = data['v12'][0]['_']

            # Conference date
            if 'v54' in data:
                citation['conf-date'] = data['v54'][0]['_']

            # Coference loc
            if 'v56' in data or 'v57' in data:
                loc = []
                if 'v56' in data:
                    loc.append(data['v56'][0]['_'])
                    if 'l' in data['v56'][0]:
                        loc.append(data['v56'][0]['l'])
                if 'v57' in data:
                    loc.append(data['v57'][0]['_'])

                citation['conf-loc'] = ", ".join(loc)

            # Conference name
            if 'v53' in data:
                citation['conf-name'] = data['v53'][0]['_']

            # Conference sponsor
            if 'v52' in data:
                citation['conf-sponsor'] = data['v52'][0]['_']

            # Citation date
            if 'v65' in data:
                citation['date'] = {}
                if data['v65'][0]['_'][6:8] != '00':
                    citation['date']['day'] = data['v65'][0]['_'][6:8]
                if data['v65'][0]['_'][4:6] != '00':
                    citation['date']['month'] = data['v65'][0]['_'][4:6]
                citation['date']['year'] = data['v65'][0]['_'][0:4]

            # Edition
            if 'v63' in data:
                citation['edition'] = data['v63'][0]['_'][0:4]

            # URL
            if 'v37' in data:
                citation['uri'] = data['v37'][0]['_']

            # Pages
            if 'v14' in data:
                page_range = data['v14'][0]['_'].split('-')
                citation['fpage'] = page_range[0]
                if len(page_range) > 1:
                    citation['lpage'] = page_range[1]

            # Institution
            citation['institutions'] = []
            if 'v11' in data:
                citation['institutions'].append(data['v11'][0]['_'])
            if 'v17' in data:
                citation['institutions'].append(data['v17'][0]['_'])
            if 'v29' in data:
                citation['institutions'].append(data['v29'][0]['_'])
            if 'v50' in data:
                citation['institutions'].append(data['v50'][0]['_'])
            if 'v58' in data:
                citation['institutions'].append(data['v58'][0]['_'])

            # ISSN
            if 'v35' in data:
                citation['issn'] = data['v35'][0]['_']

            # ISBN
            if 'v69' in data:
                citation['isbn'] = data['v69'][0]['_']

            # Volume number
            if 'v31' in data:
                citation['volume'] = data['v31'][0]['_']

            # Issue number
            if 'v32' in data:
                citation['issue'] = data['v32'][0]['_']

            # Issue title
            if 'v33' in data:
                citation['issue-title'] = data['v33'][0]['_']

            # Issue part
            if 'v34' in data:
                citation['issue-part'] = data['v34'][0]['_']

            # Citation DOI
            if 'v237' in data:
                citation['object-id'] = data['v237'][0]['_']

            # Authors analitic
            if 'v10' in data or 'v16' in data:
                citation['person-group'] = []

            if 'v10' in data:
                for author in data['v10']:
                    authordict = {}
                    if 's' in author:
                        authordict['surname'] = author['s']
                    if 'n' in author:
                        authordict['given-names'] = author['n']
                    if 's' in author or 'n' in author:
                        citation['person-group'].append(authordict)

            # Authors monographic
            if 'v16' in data:
                for author in data['v16']:
                    authordict = {}
                    if 's' in author:
                        authordict['surname'] = author['s']
                    if 'n' in author:
                        authordict['given-names'] = author['n']
                    if 's' in author or 'n' in author:
                        citation['person-group'].append(authordict)

            if 'person-group' in citation:
                if not len(citation['person-group']) > 0:
                    del citation['person-group']

            if 'v25' in data:
                citation['series'] = data['v25'][0]['_']

            if 'v62' in data:
                citation['publisher-name'] = data['v62'][0]['_']

            # Publisher loc
            if 'v66' in data or 'v67' in data:
                loc = []
                if 'v66' in data:
                    loc.append(data['v66'][0]['_'])
                    if 'e' in data['v66'][0]:
                        loc.append(data['v66'][0]['e'])
                if 'v67' in data:
                    loc.append(data['v67'][0]['_'])

                citation['publisher-loc'] = ", ".join(loc)

            citations.append(citation)

        return citations
