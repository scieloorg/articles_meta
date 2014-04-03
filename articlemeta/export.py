from xylose.scielodocument import Article
import plumber

import export_sci
import export_doaj


class Export(object):

    def __init__(self, article):
        self._article = article

    def pipeline_sci(self):
        xylose_article = Article(self._article)

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

        transformed_data = ppl.run(xylose_article, rewrap=True)

        return next(transformed_data)

    def pipeline_doaj(self):
        xylose_article = Article(self._article, iso_format='iso 639-2')

        ppl = plumber.Pipeline(export_doaj.SetupArticlePipe(),
                               export_doaj.XMLArticlePipe(),
                               export_doaj.XMLJournalMetaPublisherPipe(),
                               export_doaj.XMLJournalMetaJournalTitlePipe(),
                               export_doaj.XMLJournalMetaISSNPipe(),
                               export_doaj.XMLArticleMetaPublicationDatePipe(),
                               export_doaj.XMLArticleMetaVolumePipe(),
                               export_doaj.XMLArticleMetaIssuePipe(),
                               export_doaj.XMLArticleMetaStartPagePipe(),
                               export_doaj.XMLArticleMetaEndPagePipe(),
                               export_doaj.XMLArticleMetaArticleIdDOIPipe(),
                               export_doaj.XMLArticleMetaIdPipe(),
                               export_doaj.XMLArticleMetaDocumentTypePipe(),
                               export_doaj.XMLArticleMetaTitlePipe(),
                               export_doaj.XMLArticleMetaAuthorsPipe(),
                               export_doaj.XMLArticleMetaAffiliationPipe(),
                               export_doaj.XMLArticleMetaAbstractsPipe(),
                               export_doaj.XMLArticleMetaFullTextUrlPipe(),
                               export_doaj.XMLArticleMetaKeywordsPipe(),
                               export_doaj.XMLClosePipe())

        transformed_data = ppl.run(xylose_article, rewrap=True)

        return next(transformed_data)