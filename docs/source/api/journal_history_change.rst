=================
/journal/history/
=================

Retorna os identificadores de periódicos que sofreram modificações em um período
especificado. As mudanças possíveis são: alteração, inclusão e exclusão.

As ações de mudanças são representadas pelo atributo **event**. presente em todos
os registros de histórico de mudanças.

Recomenda-se que após feita uma coleta completa dos metadados desejados através dos
endpoints journal, issue e article, as coletas periódicas passem a utilizar o endpoint
history para atualização dos metadados de registros já copiados, para identificar novos
registros inseridos e registros excluídos do SciELO.

Parâmetros:

    +------------+-----------------------------------------------------+-------------+
    | Paremetros | Descrição                                           | Obrigatório |
    +============+=====================================================+=============+
    | collection | Acrônimo de três letras de coleções SciELO          | não         |
    +------------+-----------------------------------------------------+-------------+
    | from       | data ISO ex: 2015-01-01, padrão 1500-01-01          | não         |
    +------------+-----------------------------------------------------+-------------+
    | until      | data ISO ex: 2015-01-01, padrão data corrente       | não         |
    +------------+-----------------------------------------------------+-------------+
    | offset     | Próximos registros                                  | não         |
    +------------+-----------------------------------------------------+-------------+
    | callback   | JSONP callback method                               | não         |
    +------------+-----------------------------------------------------+-------------+

--------
Exemplos
--------

Primeiros 10 registros
======================

``GET /api/v1/journal/history/?collection=scl&from=2017-06-01&limit=10``

Resposta:

.. code-block:: json

    {

        "meta": {
            "filter": {
                "collection": "scl",
                "date": {
                    "$lte": "2017-06-28T15:02:17.415225",
                    "$gt": "2017-06-01"
                }
            },
            "limit": 10,
            "offset": 0
        },
        "objects": [
            {
                "code": "1984-7726",
                "collection": "scl",
                "date": "2017-06-10T07:42:42.629383",
                "event": "add"
            },
            {
                "code": "1413-8271",
                "collection": "scl",
                "date": "2017-06-10T07:42:51.016512",
                "event": "update"
            },
            {
                "code": "1413-8271",
                "collection": "scl",
                "date": "2017-06-10T07:42:51.978107",
                "event": "add"
            },
            {
                "code": "1413-8557",
                "collection": "scl",
                "date": "2017-06-10T07:42:53.121927",
                "event": "update"
            },
            {
                "code": "1413-8557",
                "collection": "scl",
                "date": "2017-06-10T07:42:53.123006",
                "event": "add"
            },
            {
                "code": "0102-4698",
                "collection": "scl",
                "date": "2017-06-14T23:17:13.442301",
                "event": "update"
            },
            {
                "code": "0102-4698",
                "collection": "scl",
                "date": "2017-06-14T23:17:13.443197",
                "event": "add"
            },
            {
                "code": "1678-8621",
                "collection": "scl",
                "date": "2017-06-14T23:17:23.036300",
                "event": "update"
            },
            {
                "code": "1678-8621",
                "collection": "scl",
                "date": "2017-06-14T23:17:24.320004",
                "event": "add"
            },
            {
                "code": "0101-9074",
                "collection": "scl",
                "date": "2017-06-20T18:32:19.642767",
                "event": "update"
            }
        ]

    }

Próximos 10 registros
=====================

``GET /api/v1/journal/history/?collection=scl&from=2017-06-01&limit=10&offset=11``

Resposta:

.. code-block:: json

    {

        "meta": {
            "offset": 11,
            "filter": {
                "date": {
                    "$gt": "2017-06-01",
                    "$lte": "2017-06-28T15:02:33.315415"
                },
                "collection": "scl"
            },
            "limit": 10
        },
        "objects": [
            {
                "date": "2017-06-20T18:32:23.265241",
                "collection": "scl",
                "event": "update",
                "code": "1806-4892"
            },
            {
                "date": "2017-06-20T18:32:23.829733",
                "collection": "scl",
                "event": "add",
                "code": "1806-4892"
            },
            {
                "date": "2017-06-20T18:32:23.882498",
                "collection": "scl",
                "event": "update",
                "code": "0102-3772"
            },
            {
                "date": "2017-06-20T18:32:23.883490",
                "collection": "scl",
                "event": "add",
                "code": "0102-3772"
            },
            {
                "date": "2017-06-23T17:12:02.998668",
                "collection": "scl",
                "event": "update",
                "code": "0102-4698"
            },
            {
                "date": "2017-06-23T17:12:03.112197",
                "collection": "scl",
                "event": "add",
                "code": "0102-4698"
            },
            {
                "date": "2017-06-23T17:12:09.065924",
                "collection": "scl",
                "event": "update",
                "code": "1415-9848"
            },
            {
                "date": "2017-06-23T17:12:09.066595",
                "collection": "scl",
                "event": "add",
                "code": "1415-9848"
            },
            {
                "date": "2017-06-23T17:26:07.982708",
                "collection": "scl",
                "event": "update",
                "code": "0102-4698"
            },
            {
                "date": "2017-06-23T17:26:07.983802",
                "collection": "scl",
                "event": "add",
                "code": "0102-4698"
            }
        ]

    }