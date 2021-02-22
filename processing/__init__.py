import re
import html

HTTP_SCAPE_CHARS = re.compile(".*(<http.*?>|<http.*?>?).*", re.MULTILINE)

def escape_html_http_tags(string):
    """Escapa trechos de uma string que podem ser interpretadas como tags HTML.

    >>> escape_html_http_tags("Citação disponível em <http://www.scielo.br>.")
    >>> "Citação disponível em &lt;http://www.scielo.br&gt;."
    >>> escape_html_http_tags("Citação disponível em <http://www.scielo.br")
    >>> "Citação disponível em &lt;http://www.scielo.br"
    """

    while HTTP_SCAPE_CHARS.match(string):
        match = HTTP_SCAPE_CHARS.match(string)
        http_string = match.groups()[0]
        string = string.replace(http_string, html.escape(http_string))
    return string
