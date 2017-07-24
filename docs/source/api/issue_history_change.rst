===============
/issue/history/
===============

Retorna os identificadores de fascículos que sofreram modificações em um período
especificado. As mudanças possíveis são: alteração, inclusão e exclusão.

As ações de mudanças são representadas pelo atributo **event**. presente em todos
os registros de histórico de mudanças.

Recomenda-se que após feita uma coleta completa dos metadados desejados através
dos endpoints journal, issue e article, as coletas periódicas passem a utilizar
o endpoint history para atualização dos metadados de registros já copiados, para
identificar novos registros inseridos e registros excluídos do SciELO.

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

``GET /api/v1/journal/issue/?collection=scl&from=2017-06-01&limit=10``

Resposta:

.. code-block:: json

    {
        "meta": {
            "offset": 0,
            "filter": {
                "date": {
                    "$gt": "2017-06-01",
                    "$lte": "2017-06-28T14:36:43.995233"
                },
                "collection": "scl"
            },
            "limit": 10
        },
        "objects": [
            {
                "date": "2017-06-01T05:24:51.466875",
                "collection": "scl",
                "event": "add",
                "code": "0101-206120170002"
            },
            {
                "date": "2017-06-01T05:24:51.504630",
                "collection": "scl",
                "event": "add",
                "code": "1808-238620170003"
            },
            {
                "date": "2017-06-01T05:24:51.742016",
                "collection": "scl",
                "event": "add",
                "code": "2238-387520110002"
            },
            {
                "date": "2017-06-01T05:24:51.821630",
                "collection": "scl",
                "event": "add",
                "code": "0103-847820170007"
            },
            {
                "date": "2017-06-01T05:24:51.914629",
                "collection": "scl",
                "event": "update",
                "code": "1806-371320150050"
            },
            {
                "date": "2017-06-01T05:24:51.915368",
                "collection": "scl",
                "event": "add",
                "code": "1806-371320150050"
            },
            {
                "date": "2017-06-01T05:24:52.011061",
                "collection": "scl",
                "event": "update",
                "code": "0103-058220170050"
            },
            {
                "date": "2017-06-01T05:24:52.011916",
                "collection": "scl",
                "event": "add",
                "code": "0103-058220170050"
            },
            {
                "date": "2017-06-01T05:24:52.156513",
                "collection": "scl",
                "event": "add",
                "code": "1415-527320170002"
            },
            {
                "date": "2017-06-01T05:24:52.201173",
                "collection": "scl",
                "event": "update",
                "code": "1807-257720170050"
            }
        ]
    }

Próximos 10 registros
=====================

``GET /api/v1/issue/history/?collection=scl&from=2017-06-01&limit=10&offset=11``

Resposta:

.. code-block:: json

    {

        "meta": {
            "filter": {
                "collection": "scl",
                "date": {
                    "$lte": "2017-06-28T14:36:24.608717",
                    "$gt": "2017-06-01"
                }
            },
            "limit": 10,
            "offset": 11
        },
        "objects": [
            {
                "code": "0102-330620170002",
                "collection": "scl",
                "date": "2017-06-01T05:24:52.324418",
                "event": "add"
            },
            {
                "code": "2317-643120150050",
                "collection": "scl",
                "date": "2017-06-01T05:24:52.501095",
                "event": "update"
            },
            {
                "code": "2317-643120150050",
                "collection": "scl",
                "date": "2017-06-01T05:24:52.502062",
                "event": "add"
            },
            {
                "code": "2317-153720150050",
                "collection": "scl",
                "date": "2017-06-01T05:24:52.585875",
                "event": "update"
            },
            {
                "code": "2317-153720150050",
                "collection": "scl",
                "date": "2017-06-01T05:24:52.586656",
                "event": "add"
            },
            {
                "code": "0102-672020150050",
                "collection": "scl",
                "date": "2017-06-01T05:24:52.646718",
                "event": "update"
            },
            {
                "code": "0102-672020150050",
                "collection": "scl",
                "date": "2017-06-01T05:24:52.647477",
                "event": "add"
            },
            {
                "code": "2175-623620170050",
                "collection": "scl",
                "date": "2017-06-01T05:24:52.725157",
                "event": "update"
            },
            {
                "code": "2175-623620170050",
                "collection": "scl",
                "date": "2017-06-01T05:24:52.726147",
                "event": "add"
            },
            {
                "code": "2238-387520120003",
                "collection": "scl",
                "date": "2017-06-01T05:24:52.803174",
                "event": "add"
            }
        ]

    }