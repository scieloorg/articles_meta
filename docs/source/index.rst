Servidor RPC para estatísticas de publicação
============================================

Este servidor RPC fornece um conjunto de endpoints para recuperação de
registros de artigo, periódico e coleção da Rede SciELO. Os registros retornados
representam a estrutura de dados legada do SciELO no formato JSON.

Para melhor abstração dos registros retornados por este serviço, utilizar a
biblioteca Xylose: https://github.com/scieloorg/xylose

Methods
=======

.. toctree::
   :maxdepth: 2

   dev/rpc_spec/get_collection
   dev/rpc_spec/get_collection_identifiers
   dev/rpc_spec/get_journal
   dev/rpc_spec/get_journal_identifiers
   dev/rpc_spec/get_article
   dev/rpc_spec/get_article_identifiers
   dev/rpc_spec/history_changes


Structs
=======

.. toctree::
   :maxdepth: 2

   dev/rpc_spec/structs


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`