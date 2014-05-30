# coding: utf-8
import xml.etree.ElementTree as ET
import plumber

from xylose.scielodocument import Article

import export_sci
import export_rsps
import export_doaj
import export_iahx


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
                               export_rsps.XMLArticleMetaAbstractsPipe(),
                               export_rsps.XMLArticleMetaKeywordsPipe(),
                               export_rsps.XMLArticleMetaCitationsPipe(),
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

    def pipeline_iahx(self):

        ppl = plumber.Pipeline(export_iahx.SetupDocumentPipe(),
                               export_iahx.XMLDocumentIDPipe(),
                               export_iahx.XMLCollectionPipe(),
                               export_iahx.XMLKnowledgeAreaPipe(),
                               export_iahx.XMLCenterPipe(),
                               export_iahx.XMLDocumentTypePipe(),
                               export_iahx.XMLURPipe(),
                               export_iahx.XMLAuthorsPipe(),
                               export_iahx.XMLTitlePipe(),
                               export_iahx.XMLPagesPipe(),
                               export_iahx.XMLWOKCIPipe(),
                               export_iahx.XMLWOKSCPipe(),
                               export_iahx.XMLIssueLabelPipe(),
                               export_iahx.XMLJournalTitlePipe(),
                               export_iahx.XMLOriginalLanguagePipe(),
                               export_iahx.XMLPublicationDatePipe(),
                               export_iahx.XMLAbstractPipe(),
                               export_iahx.XMLAffiliationCountryPipe(),
                               export_iahx.XMLAffiliationInstitutionPipe(),
                               export_iahx.XMLSponsorPipe(),
                               export_iahx.XMLTearDownPipe())

        xmls = ppl.run([Article(article) for article in self._article])

        #Add root document
        add = ET.Element('add')

        for xml in xmls:
          add.append(xml)

        return ET.tostring(add, encoding="utf-8", method="xml")

