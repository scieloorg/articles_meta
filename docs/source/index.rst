=======================
ARTICLEMETA Restful API
=======================

API Restful que fornece um conjunto de endpoints para recuperação de
registros de artigo, periódico, fascículos e coleção da Rede SciELO. Os registros
retornados representam a estrutura de dados legada do SciELO no formato JSON.

Current version: 1.32.25

API URL: http://articlemeta.scielo.org

---------
Libraries
---------

articlemetaapi
==============

Articlemetaapi é uma biblioteca Python compatível com Python3 e Python2, desenvolvida
para facilitar a interação com a API ArticleMeta.

Esta biblioteca já utiliza a bibloteca Xylose para abstração dos metadados entregues
pela API.

Para informações sobre uso, acesse o repositório em: https://github.com/scieloorg/articlemetaapi

Como Instalar
-------------

pip install articlemetaapi

xylose
======

Xylose é uma biblioteca Python compatível com Python 3 e Python 2. Esta biblioteca
abstrai a complexidade dos registros entregues pela API.

Quando iterando com a API diretamente pelos endpoints HTTP, sem o uso da biblioteca
articlemetaapi, utiliza a biblioteca Xylose para abstração dos registros retornados.

Para informações sobre uso, acesse o repositório em: https://github.com/scieloorg/xylose

Como Instalar
-------------

pip install xylose

-------
Methods
-------

.. toctree::
   :maxdepth: 2

   api/collection
   api/collection_identifiers
   api/journal
   api/journal_identifiers
   api/journal_history_changes
   api/issue
   api/issue_identifiers
   api/issue_history_changes
   api/article
   api/article_identifiers
   api/article_history_changes

-------
Structs
-------

.. toctree::
   :maxdepth: 2

   dev/rpc_spec/structs


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
