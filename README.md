# Articles Meta


[![Build Status](https://travis-ci.org/scieloorg/articles_meta.svg)](https://travis-ci.org/scieloorg/articles_meta)
[![a](https://images.microbadger.com/badges/image/scieloorg/articles_meta.svg)](https://hub.docker.com/r/scieloorg/articles_meta)
[![b](https://images.microbadger.com/badges/version/scieloorg/articles_meta.svg)](https://hub.docker.com/r/scieloorg/articles_meta)


Webservices para fornecer metadados de artigos SciELO da Rede SciELO (armazenados no MongoDB).

## Como utilizar esta imagem

```shell
    $ docker run --name my-articlemeta -d my-articlemeta
```


### Como configurar o MONGODB_HOST

```shell
    $ docker run --name my-articlemeta -e MONGODB_HOST=my_eshost:27017 -d my-articlemeta my-articlemeta
```

Os serviços ativos nesta imagem são:

 * Web API: 127.0.0.1:8000
 * Thrift Server: 127.0.0.1:11620


É possível mapear essas portas para o hosting dos containers da seguinte forma:

```shell
    $ docker run --name my-articlemeta -e MONGODB_HOST=my_eshost:27017 -p 8000:8000 -p 11620:11620 -d my-articlemeta my-articlemeta
```

# Como executar comandos de processamentos

Para executar os processamentos disponíveis em console scripts, executar:

Carga de Licenças de uso:

```shell
   $ docker exec -i -t my-articlemeta articlemeta_loadlicenses --help
```

### Fixtures

Procedimento para popular a instância de desenvolvimento a partir de fixtures disponibilizadas pelo SciELO.

1. Para execução dos procedimentos que adicionam dados no banco é necessário que o ambiente de desenvolvimento do article_meta esteja rodando a aplicação
2. Baixar a fixture de desenvolvimento versão light com 4 periódicos, execute: ``wget https://minio.scielo.br/dev/fixtures/article_meta.zip`` 
3. Extraia o conteúdo, execute: ``unzip article_meta.zip``
4. Repare que uma pasta chamada article_meta foi criada e dentro dela há arquivos .bson, .json.
5. Acesse a pasta **article_meta**, execute: ``cd article_meta``
6. Utilizando **mongorestore** realize a recuperação do banco de dados apontando para o endereço que está rodando o seu mongo local, exemplo: ``mongorestore --host=localhost --port=27017 --db=articlemeta --dir .``


# Nota

Para histórico de desenvolvimento anterior ao registrado neste repositório, verificar: https://bitbucket.org/scieloorg/xmlwos
