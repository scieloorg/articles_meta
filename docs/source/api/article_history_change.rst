=================
/article/history/
=================

Retorna os identificadores de documentos que sofreram modificações em um período especificado. As mudanças possíveis são: alteração, inclusão e exclusão.

As ações de mudanças são representadas pelo atributo **event**. presente em todos os registros de histórico de mudanças.

Recomenda-se que após feita uma coleta completa dos metadados desejados através dos endpoints journal, issue e article, as coletas periódicas passem a utilizar o endpoint history para atualização dos metadados de registros já copiados, para identificar novos registros inseridos e registros excluídos do SciELO.

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

``GET /api/v1/article/history/?collection=scl&limit=10``

Resposta:

.. code-block:: json

    {

        "meta": {
            "filter": {
                "collection": "scl",
                "date": {
                    "$lte": "2017-06-28T14:26:36.293955",
                    "$gt": "2017-06-01"
                }
            },
            "limit": 10,
            "offset": 0
        },
        "objects": [
            {
                "code": "S0100-879X2017000600604",
                "collection": "scl",
                "date": "2017-06-01T05:24:12.234478",
                "event": "update"
            },
            {
                "code": "S0100-879X2017000600604",
                "collection": "scl",
                "date": "2017-06-01T05:24:12.236412",
                "event": "add"
            },
            {
                "code": "S0004-28032017000100041",
                "collection": "scl",
                "date": "2017-06-01T05:24:14.526611",
                "event": "update"
            },
            {
                "code": "S0004-28032017000100041",
                "collection": "scl",
                "date": "2017-06-01T05:24:14.529849",
                "event": "add"
            },
            {
                "code": "S2238-38752011000200053",
                "collection": "scl",
                "date": "2017-06-01T05:24:15.662675",
                "event": "add"
            },
            {
                "code": "S0001-37652017000200469",
                "collection": "scl",
                "date": "2017-06-01T05:24:16.096367",
                "event": "add"
            },
            {
                "code": "S1516-31802017005007106",
                "collection": "scl",
                "date": "2017-06-01T05:24:16.347640",
                "event": "add"
            },
            {
                "code": "S0001-37652017000200431",
                "collection": "scl",
                "date": "2017-06-01T05:24:16.445228",
                "event": "add"
            },
            {
                "code": "S0001-37652017000200445",
                "collection": "scl",
                "date": "2017-06-01T05:24:16.688339",
                "event": "add"
            },
            {
                "code": "S0034-70942017000300227",
                "collection": "scl",
                "date": "2017-06-01T05:24:17.109051",
                "event": "add"
            }
        ]

    }

Próximos 10 registros
=====================

``GET /api/v1/article/history/?collection=scl&limit=10&offset=11``

Resposta:

.. code-block:: json

    {

        "meta": {
            "offset": 11,
            "filter": {
                "date": {
                    "$gt": "2017-06-01",
                    "$lte": "2017-06-28T14:28:06.632830"
                },
                "collection": "scl"
            },
            "limit": 10
        },
        "objects": [
            {
                "date": "2017-06-01T05:24:17.482582",
                "collection": "scl",
                "event": "add",
                "code": "S1980-50982011000300421"
            },
            {
                "date": "2017-06-01T05:24:17.706487",
                "collection": "scl",
                "event": "update",
                "code": "S0104-07072017000100601"
            },
            {
                "date": "2017-06-01T05:24:17.707738",
                "collection": "scl",
                "event": "add",
                "code": "S0104-07072017000100601"
            },
            {
                "date": "2017-06-01T05:24:18.153251",
                "collection": "scl",
                "event": "add",
                "code": "S0101-20612017000200269"
            },
            {
                "date": "2017-06-01T05:24:18.292193",
                "collection": "scl",
                "event": "add",
                "code": "S2238-38752012000400295"
            },
            {
                "date": "2017-06-01T05:24:18.554442",
                "collection": "scl",
                "event": "add",
                "code": "S0103-84782017000700601"
            },
            {
                "date": "2017-06-01T05:24:18.866931",
                "collection": "scl",
                "event": "update",
                "code": "S2176-66812016000300619"
            },
            {
                "date": "2017-06-01T05:24:18.867917",
                "collection": "scl",
                "event": "add",
                "code": "S2176-66812016000300619"
            },
            {
                "date": "2017-06-01T05:24:19.376787",
                "collection": "scl",
                "event": "add",
                "code": "S1980-50982011000100103"
            },
            {
                "date": "2017-06-01T05:24:19.431559",
                "collection": "scl",
                "event": "add",
                "code": "S2238-38752011000200077"
            }
        ]

    }