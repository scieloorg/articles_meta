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
para facilitar a interação com a API ArticleMeta. Esta biblioteca já utiliza a bibloteca 
Xylose para abstração dos metadados entregues pela API.

Para informações sobre uso, acesse o repositório em: https://github.com/scieloorg/articlemetaapi

xylose
======

Xylose é uma biblioteca Python compatível com Python 3 e Python 2. Esta biblioteca
abstrai a complexidade dos registros entregues pela API.

Quando iterando com a API diretamente pelos endpoints HTTP, sem o uso da biblioteca
articlemetaapi, utiliza a biblioteca Xylose para abstração dos registros retornados.

Para informações sobre uso, acesse o repositório em: https://github.com/scieloorg/xylose

----------------
Arquivos em lote
----------------

Para carga inicial de metadados recomendamos o download e processamento dos arquivos
em lote, os arquivos em lote possuem todos os resultados de todos os registros da
API ArticleMeta e são atualizados mensalmente.

Gere sua base de dados a partir dos arquivos em lote, e posteriormente utilize os
endpoints de histórico de mudanças para atualizar sua base de dados.

O download de todos os registros da API através do protocolo HTTP podem levar em
média 3,5 dias. Esse tempo pode varia dependendo de sua conectividade, da capacidade
de throughput da API entre outras variáveis.

Ao utilizar os arquivos em lote esse tempo pode ser reduzido para poucas horas de download.

Baixar o arquivo em lote em: http://static.scielo.org/articlemeta/articles.json.zip

-------
Métodos
-------

.. toctree::
   :maxdepth: 2

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
