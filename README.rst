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



Docker
======

Instalação do docker-compose
----------------------------

.. code-block::

    $> pip install -U docker-compose


Build & Run com docker-compose
------------------------------

.. code-block::

    $> cd <repositório>
    $> docker-compose up --build


Restaurando dados ao mongodb
----------------------------

- é preciso identificar o local e porta do container mongo.
- é preciso ter instalado o cliente mongo (mongorestore)
- o volume com os dados do container mongo, estão linkados a: /opt/articlemeta_mongo/data (veja docker-compose.yml)

.. code-block::

    $ cd <repositório>
    $ docker-compose up
    $ cd <pasta com os dados a restaurar>
    $ mongorestore --host localhost:27017 --gzip --archive articlemeta


Acessando
---------

- O servidor web esta escutando em localhost:8000
- O mongodb esta escutando em localhost:27017
- O servidor Thrift esta escutando em localhost:11620

Para ajustar estas portas, deve editar e ser consistente, nos arquivos:

- Dockerfile
- docker/generate_production_ini.py
- docker-entrypoint.sh
