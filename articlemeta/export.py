from xylose.scielodocument import Article
import plumber

import export_sci
import export_doaj


class Export(object):

    def __init__(self, article):
        self._article = Article(article)

    def pipeline_sci(self):

        ppl = plumber.Pipeline(export_sci.SetupArticlePipe(),
                               export_sci.XMLArticlePipe(),
                               export_sci.XMLFrontBackPipe(),
                               export_sci.XMLJournalMetaJournalIdPipe(),
                               export_sci.XMLJournalMetaJournalTitleGroupPipe(),
                               export_sci.XMLJournalMetaISSNPipe(),
                               export_sci.XMLJournalMetaPublisherPipe(),
                               export_sci.XMLArticleMetaUniqueArticleIdPipe(),
                               export_sci.XMLArticleMetaArticleIdPublisherPipe(),
                               export_sci.XMLArticleMetaArticleIdDOIPipe(),
                               export_sci.XMLArticleMetaArticleCategoriesPipe(),
                               export_sci.XMLArticleMetaTitleGroupPipe(),
                               export_sci.XMLArticleMetaTranslatedTitleGroupPipe(),
                               export_sci.XMLArticleMetaContribGroupPipe(),
                               export_sci.XMLArticleMetaAffiliationPipe(),
                               export_sci.XMLArticleMetaGeneralInfoPipe(),
                               export_sci.XMLArticleMetaAbstractsPipe(),
                               export_sci.XMLArticleMetaKeywordsPipe(),
                               export_sci.XMLArticleMetaCitationsPipe(),
                               export_sci.XMLClosePipe())

        transformed_data = ppl.run(self._article, rewrap=True)

        return next(transformed_data)

    def pipeline_doaj(self):

        ppl = plumber.Pipeline(export_doaj.SetupArticlePipe(),
                               export_doaj.XMLArticlePipe(),
                               export_doaj.XMLFrontBackPipe(),
                               export_doaj.XMLJournalMetaJournalIdPipe(),
                               export_doaj.XMLJournalMetaJournalTitleGroupPipe(),
                               export_doaj.XMLJournalMetaISSNPipe(),
                               export_doaj.XMLJournalMetaPublisherPipe(),
                               export_doaj.XMLArticleMetaUniqueArticleIdPipe(),
                               export_doaj.XMLArticleMetaArticleIdPublisherPipe(),
                               export_doaj.XMLArticleMetaArticleIdDOIPipe(),
                               export_doaj.XMLArticleMetaArticleCategoriesPipe(),
                               export_doaj.XMLArticleMetaTitleGroupPipe(),
                               export_doaj.XMLArticleMetaTranslatedTitleGroupPipe(),
                               export_doaj.XMLArticleMetaContribGroupPipe(),
                               export_doaj.XMLArticleMetaAffiliationPipe(),
                               export_doaj.XMLArticleMetaGeneralInfoPipe(),
                               export_doaj.XMLArticleMetaAbstractsPipe(),
                               export_doaj.XMLArticleMetaKeywordsPipe(),
                               export_doaj.XMLClosePipe())

        transformed_data = ppl.run(self._article, rewrap=True)

        return next(transformed_data)