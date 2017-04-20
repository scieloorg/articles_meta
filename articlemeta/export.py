# coding: utf-8
import plumber

from xylose.scielodocument import Article

from articlemeta import export_sci
from articlemeta import export_rsps
from articlemeta import export_doaj
from articlemeta import export_pubmed
from articlemeta import export_crossref


class Export(object):

    def __init__(self, article):
        self._article = article

    def pipeline_sci(self):
        xylose_article = Article(self._article)

        ppl = plumber.Pipeline(export_sci.SetupArticlePipe(),
                               export_sci.XMLArticlePipe(),
                               export_sci.XMLFrontPipe(),
                               export_sci.XMLJournalMetaJournalIdPipe(),
                               export_sci.XMLJournalMetaJournalTitleGroupPipe(),
                               export_sci.XMLJournalMetaISSNPipe(),
                               export_sci.XMLJournalMetaCollectionPipe(),
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
                               export_sci.XMLArticleMetaPermissionPipe(),
                               export_sci.XMLArticleMetaURLsPipe(),
                               export_sci.XMLArticleMetaAbstractsPipe(),
                               export_sci.XMLArticleMetaKeywordsPipe(),
                               export_sci.XMLArticleMetaCitationsPipe(),
                               export_sci.XMLClosePipe())

        transformed_data = ppl.run(xylose_article, rewrap=True)

        return next(transformed_data)

    def pipeline_rsps(self):
        xylose_article = Article(self._article)

        ppl = plumber.Pipeline(export_rsps.SetupArticlePipe(),
                               export_rsps.XMLArticlePipe(),
                               export_rsps.XMLFrontPipe(),
                               export_rsps.XMLJournalMetaJournalIdPipe(),
                               export_rsps.XMLJournalMetaJournalTitleGroupPipe(),
                               export_rsps.XMLJournalMetaISSNPipe(),
                               export_rsps.XMLJournalMetaPublisherPipe(),
                               export_rsps.XMLArticleMetaArticleIdPublisherPipe(),
                               export_rsps.XMLArticleMetaArticleIdDOIPipe(),
                               export_rsps.XMLArticleMetaArticleCategoriesPipe(),
                               export_rsps.XMLArticleMetaTitleGroupPipe(),
                               export_rsps.XMLArticleMetaTranslatedTitleGroupPipe(),
                               export_rsps.XMLArticleMetaContribGroupPipe(),
                               export_rsps.XMLArticleMetaAffiliationPipe(),
                               export_rsps.XMLArticleMetaGeneralInfoPipe(),
                               export_rsps.XMLArticleMetaHistoryPipe(),
                               export_rsps.XMLArticleMetaPermissionPipe(),
                               export_rsps.XMLArticleMetaAbstractsPipe(),
                               export_rsps.XMLArticleMetaKeywordsPipe(),
                               export_rsps.XMLArticleMetaCountsPipe(),
                               export_rsps.XMLBodyPipe(),
                               export_rsps.XMLArticleMetaCitationsPipe(),
                               export_rsps.XMLSubArticlePipe(),
                               export_rsps.XMLClosePipe())

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

    def pipeline_pubmed(self):
        xylose_article = Article(self._article, iso_format='iso 639-2')

        ppl = plumber.Pipeline(export_pubmed.SetupArticleSetPipe(),
                               export_pubmed.XMLArticlePipe(),
                               export_pubmed.XMLJournalPipe(),
                               export_pubmed.XMLPublisherNamePipe(),
                               export_pubmed.XMLJournalTitlePipe(),
                               export_pubmed.XMLISSNPipe(),
                               export_pubmed.XMLVolumePipe(),
                               export_pubmed.XMLIssuePipe(),
                               export_pubmed.XMLPubDatePipe(),
                               export_pubmed.XMLReplacesPipe(),
                               export_pubmed.XMLArticleTitlePipe(),
                               export_pubmed.XMLFirstPagePipe(),
                               export_pubmed.XMLLastPagePipe(),
                               export_pubmed.XMLElocationIDPipe(),
                               export_pubmed.XMLLanguagePipe(),
                               export_pubmed.XMLAuthorListPipe(),
                               export_pubmed.XMLPublicationTypePipe(),
                               export_pubmed.XMLArticleIDListPipe(),
                               export_pubmed.XMLHistoryPipe(),
                               export_pubmed.XMLAbstractPipe(),
                               export_pubmed.XMLClosePipe())

        transformed_data = ppl.run(xylose_article, rewrap=True)

        return next(transformed_data)

    def pipeline_crossref(self):
        xylose_article = Article(self._article)

        ppl = plumber.Pipeline(
            export_crossref.SetupDoiBatchPipe(),
            export_crossref.XMLHeadPipe(),
            export_crossref.XMLBodyPipe(),
            export_crossref.XMLDoiBatchIDPipe(),
            export_crossref.XMLTimeStampPipe(),
            export_crossref.XMLDepositorPipe(),
            export_crossref.XMLRegistrantPipe(),
            export_crossref.XMLJournalPipe(),
            export_crossref.XMLJournalMetadataPipe(),
            export_crossref.XMLJournalTitlePipe(),
            export_crossref.XMLAbbreviatedJournalTitlePipe(),
            export_crossref.XMLISSNPipe(),
            export_crossref.XMLJournalIssuePipe(),
            export_crossref.XMLPubDatePipe(),
            export_crossref.XMLVolumePipe(),
            export_crossref.XMLIssuePipe(),
            export_crossref.XMLJournalArticlePipe(),
            export_crossref.XMLArticleTitlesPipe(),
            export_crossref.XMLArticleTitlePipe(),
            export_crossref.XMLArticleContributorsPipe(),
            export_crossref.XMLArticleAbstractPipe(),
            export_crossref.XMLArticlePubDatePipe(),
            export_crossref.XMLPagesPipe(),
            export_crossref.XMLPIDPipe(),
            export_crossref.XMLDOIDataPipe(),
            export_crossref.XMLCollectionPipe(),
            export_crossref.XMLArticleCitationsPipe(),
            export_crossref.XMLClosePipe()
        )

        transformed_data = ppl.run(xylose_article, rewrap=True)

        return next(transformed_data)