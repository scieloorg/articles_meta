Articles Meta
=============

Webservices para recuperar metadados de artigos SciELO armazenados no MongoDB.

    Para histórico de desenvolvimento anterior ao registrado neste repositório, verificar: https://bitbucket.org/scieloorg/xmlwos

.. image:: https://travis-ci.org/scieloorg/articles_meta.svg
    :target: https://travis-ci.org/scieloorg/articles_meta
    
Instalação
==========

Requisitos
----------

 * Python 2.7
 * MongoDB
 * virtualenvwrapper
 * pip
 
Passos para Instalação
----------------------

#. Criar ambiente virtual

.. code-block::

    #> mkvirtualenv articles_meta
    #> workon articles_meta

#. Baixar última versão
#. Descompactar
#. Acessar diretório articles_meta<version>
#. Instalar dependências

.. code-block::

    #> pip install -r requirements.txt
    
#. Configurar aplicação

.. code-block::

    #> cp development.ini-TEMPLATE development.ini
    #> vi development.ini
    
#. Editar parâmetros

.. code-block::

    mongo_uri = mongodb://node1-mongodb.scielo.org:27000/articlemeta
    admintoken = anyhashcode
    
#. Iniciar aplicação

.. code-block::

    #> pserve development.ini
    
#. Iniciar RPC server

.. code-block::

    #> articlemeta_thrift_server --port 11620 --host 0.0.0.0
