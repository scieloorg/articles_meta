# coding: utf-8
import unittest

from processing import load_licenses

class LoadLicensesTest(unittest.TestCase):

    def test_scrapt_license_by(self):

        data = """5&amp;lng=en','','width=640,height=500,resizable=yes,scrollbars=1,menubar=yes,');">Links</a> ] </p></div><div class="foot-notes"><a name="fn01"></a><p class="fn"><a href="#back_fn01" class="fn-label">1</a> Part of first author's PhD thesis</p></div></div><div class="foot-notes"><div class="history"><p>Received:
                    June23, , 2014; Accepted:
                    November11, , 2014</p></div><div class="author-notes"><p class="corresp"><a name="c01"></a>* <strong>Corresponding author:</strong>
               <a href="mailto:ribeirosenna1@gmail.com">ribeirosenna1@gmail.com</a>
            </p></div></div><div class="foot-notes"><p><a rel="license" href="http://creativecommons.org/licenses/by/4.0//deed.en"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by/4.0//88x31.png"></a><p class="first" id="license-p">This is an Open Access article distributed under the terms of the Creative
                  Commons Attribution Non-Commercial License, which permits unrestricted
                  non-commercial use, distribution, and reproduction in any medium, provided the
                  original work is properly cited.</p></p></div></div></div></div>"""

        result = load_licenses.scrap_license(data)

        self.assertEqual(result, 'by/4.0')

    def test_scrapt_license_by_nc(self):

        data = """5&amp;lng=en','','width=640,height=500,resizable=yes,scrollbars=1,menubar=yes,');">Links</a> ] </p></div><div class="foot-notes"><a name="fn01"></a><p class="fn"><a href="#back_fn01" class="fn-label">1</a> Part of first author's PhD thesis</p></div></div><div class="foot-notes"><div class="history"><p>Received:
                    June23, , 2014; Accepted:
                    November11, , 2014</p></div><div class="author-notes"><p class="corresp"><a name="c01"></a>* <strong>Corresponding author:</strong>
               <a href="mailto:ribeirosenna1@gmail.com">ribeirosenna1@gmail.com</a>
            </p></div></div><div class="foot-notes"><p><a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0//deed.en"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc/4.0//88x31.png"></a><p class="first" id="license-p">This is an Open Access article distributed under the terms of the Creative
                  Commons Attribution Non-Commercial License, which permits unrestricted
                  non-commercial use, distribution, and reproduction in any medium, provided the
                  original work is properly cited.</p></p></div></div></div></div>"""

        result = load_licenses.scrap_license(data)

        self.assertEqual(result, 'by-nc/4.0')

    def test_scrapt_license_just_img(self):

        data = """5&amp;lng=en','','width=640,height=500,resizable=yes,scrollbars=1,menubar=yes,');">Links</a> ] </p></div><div class="foot-notes"><a name="fn01"></a><p class="fn"><a href="#back_fn01" class="fn-label">1</a> Part of first author's PhD thesis</p></div></div><div class="foot-notes"><div class="history"><p>Received:
                    June23, , 2014; Accepted:
                    November11, , 2014</p></div><div class="author-notes"><p class="corresp"><a name="c01"></a>* <strong>Corresponding author:</strong>
               <a href="mailto:ribeirosenna1@gmail.com">ribeirosenna1@gmail.com</a>
            </p></div></div><div class="foot-notes"><p><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc/4.0//88x31.png"></a><p class="first" id="license-p">This is an Open Access article distributed under the terms of the Creative
                  Commons Attribution Non-Commercial License, which permits unrestricted
                  non-commercial use, distribution, and reproduction in any medium, provided the
                  original work is properly cited.</p></p></div></div></div></div>"""

        result = load_licenses.scrap_license(data)

        self.assertEqual(result, 'by-nc/4.0')

    def test_scrap_license_t1(self):

        data = """
            il: <a href="mailto:ipem@evangelico.org.br">ipem@evangelico.org.br</a></font></p>
            <p><font size="2" face="Verdana">Conflito de interesse: n&atilde;o h&aacute;    <br>   Fonte financiadora: n&atilde;o h&aacute;    
            <br>   Recebido para publica&ccedil;&atilde;o em: 11/05/2007    <br>   Aceito para publica&ccedil;&atilde;o em: 21/09/2007</font></p>  
                </div></div><div class="footer"><p><a rel="license" href="/deed.en">
                <img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/88x31.png"></a>
                All the contents of this journal, except where otherwise noted, is licensed under a <a href="/deed.en">Creative Commons Attribution License</a></p><p><i>Colégio Brasileiro de Cirurgia Digestiva - CBCD</i></p>Av. Brigadeiro Luiz Antonio, 278 - 6° - Salas 10 e 11<br>01318-901 São Paulo/SP Brasil<br>Tel.: (11) 3288-8174/3289-0741<br><IMG src="/img/en/e-mailt.gif" border="0"><br><A class="email" href="mailto:secretaria@cbcd.org.br">secretaria@cbcd.org.br</A><img src="http://scielo-log.scielo.br/scielolog/updateLog02.php?app=scielo&amp;page=sci_arttext&amp;pid=S0102-67202008000100007&amp;lang=en&amp;norm=iso&amp;doctopic=tr&amp;doctype=article&amp;tlng=en" border="0" height="1" width="1"><script type="text/javascript">
                          var _paq = _paq || [];
                          _paq.push(["setDocumentTitle", document.domain + "/" + document.title]);
                          _paq.push(["setCookieDomain", "*.
        """

        result = load_licenses.scrap_license(data)

        self.assertEqual(result, None)


    def test_scrap_license_t2(self):

        data = """
            and the Caribbean. Washington: The World Bank; 2002. (World Bank Discussion 
            Paper, 433).</font></p> <!-- fim arquivo --> </div></div><!--cc--><!--mode=license--><!--GENERAL_LICENSE-->
            <!--scielo-fulltext match=permissions--><div class="license"><!-- default_license_href=http://creativecommons.org/licenses/by/4.0-->
            <!-- lang_license_href=http://creativecommons.org/licenses/by/4.0/deed.en-->
            <!-- license_href=http://creativecommons.org/licenses/by/4.0/-->
            <!-- license_img_src=http://i.creativecommons.org/l/by/4.0/80x15.png-->
            <!-- $lang_license_href!='' and $license_img_src!='' --><p>
            <a rel="license" href="http://creativecommons.org/licenses/by/4.0/deed.en">
            <img src="http://i.creativecommons.org/l/by/4.0/80x15.png" alt="Creative Commons License" style="border-width:0">
            </a></p></div><div class="footer">Avenida Dr. Arnaldo, 715<br>01246-904 São Paulo SP Brazil<br>Tel./Fax: +55 11 3061-7985<br>
            <IMG src="/img/en/e-mailt.gif" border="0"><br><A class="email" href="mailto:revsp@org.usp.br">revsp@org.usp.br</A>
            <img src="http://scielo-log.scielo.br/scielolog/updateLog02.php?app=scielo&amp;page=sci_arttext&amp;pid=S0034-89102010000200006&amp;lang=en&amp;norm=iso&amp;doctopic=oa&amp;doctype=article&amp;tlng=en" border="0" height="1" width="1"></div></div><!----></body></html>        """

        result = load_licenses.scrap_license(data)

        self.assertEqual(result, 'by/4.0')

    def test_scrap_license_t3(self):

        data = """
            <div xmlns="" class="container"><div align="left"></div><div class="spacer"> </div><!--cc--><!--mode=license--><!--GENERAL_LICENSE--><!--scielo-fulltext match=permissions--><div class="license"><!-- default_license_href=http://creativecommons.org/licenses/by/4.0--><!-- lang_license_href=http://creativecommons.org/licenses/by/4.0/deed.en--><!-- license_href=http://creativecommons.org/licenses/by/4.0/--><!-- license_img_src=http://i.creativecommons.org/l/by/4.0/80x15.png--><!-- $lang_license_href!='' and $license_img_src!='' --><p><a rel="license" href="http://creativecommons.org/licenses/by/4.0/deed.en"><img src="http://i.creativecommons.org/l/by/4.0/80x15.png" alt="Creative Commons License" style="border-width:0"></a></p></div><div class="footer">Av. Brasil, 4365 -  Pavilhão Mourisco, Manguinhos<br>21040-900 Rio de Janeiro RJ Brazil<br>Tel.: (55 21) 2562-1222<br>Fax: (55 21) 2562 1220<br><IMG src="/img/en/e-mailt.gif" border="0"><br><A class="email" href="mailto:memorias@fiocruz.br">memorias@fiocruz.br</A><img src="http://scielo-log.scielo.br/scielolog/updateLog02.php?app=scielo&amp;page=sci_arttext&amp;pid=S0074-02761995000100009&amp;lang=en&amp;norm=iso&amp;doctopic=oa&amp;doctype=text&amp;tlng=en" border="0" height="1" width="1"></div></div><!----></body></html>
        """

        result = load_licenses.scrap_license(data)

        self.assertEqual(result, 'by/4.0')
