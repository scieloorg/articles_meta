=============
Articles Meta
=============

.. image:: https://travis-ci.org/scieloorg/articles_meta.svg
    :target: https://travis-ci.org/scieloorg/articles_meta

.. image:: https://images.microbadger.com/badges/image/scieloorg/articles_meta.svg
    :target: https://hub.docker.com/r/scieloorg/articles_meta

.. image:: https://images.microbadger.com/badges/version/scieloorg/articles_meta.svg
    :target: https://hub.docker.com/r/scieloorg/articles_meta



Webservices para fornecer metadados de artigos SciELO da Rede SciELO (armazenados no MongoDB).


=========================
Como utilizar esta imagem
=========================

.. code-block::

    $ docker run --name my-articlemeta -d my-articlemeta


Como configurar o MONGODB_HOST
------------------------------

.. code-block::

    $ docker run --name my-articlemeta -e MONGODB_HOST=my_eshost:27017 -d my-articlemeta my-articlemeta


Os serviços ativos nesta imagem são:

* Web API: 127.0.0.1:8000
* Thrift Server: 127.0.0.1:11620

É possível mapear essas portas para o hosting dos containers da seguinte forma:

.. code-block::

    $ docker run --name my-articlemeta -e MONGODB_HOST=my_eshost:27017 -p 8000:8000 -p 11620:11620 -d my-articlemeta my-articlemeta

Como executar comandos de processamentos 
----------------------------------------
Para executar os processamentos disponíveis em console scripts, executar:

Carga de Licenças de uso:

.. code-block::

   $ docker exec -i -t my-articlemeta articlemeta_loadlicenses --help


====
Nota
====

Para histórico de desenvolvimento anterior ao registrado neste repositório, verificar: https://bitbucket.org/scieloorg/xmlwos
