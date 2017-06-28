.. toctree::
   :maxdepth: 3

   index

=======================
ARTICLEMETA Restful API
=======================

API Restful que fornece um conjunto de endpoints para recuperação de
registros de artigo, periódico, fascículos e coleção da Rede SciELO. Os registros
retornados representam a estrutura de dados legada do SciELO no formato JSON.

Versão corrente: 1.32.25

API URL: http://articlemeta.scielo.org

-----------
Bibliotecas
-----------

articlemetaapi
==============

Articlemetaapi é uma biblioteca Python compatível com Python3 e Python2, desenvolvida
para facilitar a interação com a API ArticleMeta.

Esta biblioteca já utiliza a bibloteca Xylose para abstração dos metadados entregues
pela API.

Para informações sobre uso, acesse o repositório em: https://github.com/scieloorg/articlemetaapi

xylose
======

Xylose é uma biblioteca Python compatível com Python 3 e Python 2. Esta biblioteca
abstrai a complexidade dos registros entregues pela API.

Quando iterando com a API diretamente pelos endpoints HTTP, sem o uso da biblioteca
articlemetaapi, utiliza a biblioteca Xylose para abstração dos registros retornados.

Para informações sobre uso, acesse o repositório em: https://github.com/scieloorg/xylose

-------
Métodos
-------

.. toctree::

   api/collection
   api/collection_identifiers
   api/journal
   api/journal_identifiers
   api/journal_history_change
   api/issue
   api/issue_identifiers
   api/issue_history_change
   api/article
   api/article_identifiers
   api/article_history_change


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
