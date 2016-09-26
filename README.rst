Articles Meta
=============

Webservices para recuperar metadados de artigos SciELO armazenados no MongoDB.

    Para histórico de desenvolvimento anterior ao registrado neste repositório, verificar: https://bitbucket.org/scieloorg/xmlwos

Build Status
============

.. image:: https://travis-ci.org/scieloorg/articles_meta.svg
    :target: https://travis-ci.org/scieloorg/articles_meta

Docker Status
=============

.. image:: https://images.microbadger.com/badges/image/scieloorg/articles_meta.svg
    :target: https://hub.docker.com/r/scieloorg/articles_meta
    
.. image:: https://images.microbadger.com/badges/version/scieloorg/articles_meta.svg
    :target: https://hub.docker.com/r/scieloorg/articles_meta


Como utilizar esta imagem
=========================

$ docker run --name my-articlemeta -d my-articlemeta

Como configurar o MONGODB_HOST

$ docker run --name my-articlemeta -e MONGODB_HOST=my_eshost:27017 -d my-articlemeta my-articlemeta

Os serviços ativos nesta imagem são:

Web API: 127.0.0.1:8000
Thrift Server: 127.0.0.1:11620

É possível mapear essas portas para o hosting dos containers da seguinte forma:

$ docker run --name my-articlemeta -e MONGODB_HOST=my_eshost:27017 -p 8000:8000 -p 11620:11620 -d my-articlemeta my-articlemeta

Para executar os processamentos disponíveis em console scripts, executar:

Carga de Licenças de uso:

$ docker exec -i -t my-articlemeta articlemeta_loadlicenses --help
