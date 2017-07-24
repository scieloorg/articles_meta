=====================
/article/identifiers/
=====================

Retorna uma lista de identificadores de artigos.

Parâmetros:

    +------------+-----------------------------------------------------+-------------+
    | Paremetros | Descrição                                           | Obrigatório |
    +============+=====================================================+=============+
    | issn       | ISSN do periódico no SciELO                         | não         |
    +------------+-----------------------------------------------------+-------------+
    | collection | Acrônimo de três letras de coleções SciELO          | não         |
    +------------+-----------------------------------------------------+-------------+
    | limit      | Total de registros por requisição, máximo 1000.     | não         |
    +------------+-----------------------------------------------------+-------------+
    | from       | data ISO ex: 2015-01-01, padrão 1500-01-01          | não         |
    +------------+-----------------------------------------------------+-------------+
    | until      | data ISO ex: 2015-01-01, padrão data corrente       | não         |
    +------------+-----------------------------------------------------+-------------+
    | offset     | Próximos registros                                  | não         |
    +------------+-----------------------------------------------------+-------------+
    | callback   | JSONP callback method                               | não         |
    +------------+-----------------------------------------------------+-------------+


Parâmetros obrigatórios:

    Não existem parâmetros obrigatórios

--------
Exemplos
--------

Primeiros 10 registros
======================

``GET /api/v1/article/identifiers/limit=10``

Resposta:

.. code-block:: json

    {

        "meta": {
            "filter": {
                "processing_date": {
                    "$lte": "2017-06-28",
                    "$gte": "1500-01-01"
                }
            },
            "limit": 10,
            "offset": 0
        },
        "objects": [
            {
                "code": "S0100-879X1998000800006",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000800006",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000800011",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000800011",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000800009",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000800009",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000800010",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000800010",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000800008",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000800008",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000900006",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000900006",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000800007",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000800007",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000800004",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000800004",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000800002",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000800002",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000900005",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000900005",
                "processing_date": "1998-09-21"
            }
        ]

    }

Próximos 10 registros
=====================

``GET /api/v1/article/identifiers/limit=10&offset=100``

Resposta:

.. code-block:: json

    {

        "meta": {
            "filter": {
                "processing_date": {
                    "$lte": "2017-06-28",
                    "$gte": "1500-01-01"
                }
            },
            "limit": 10,
            "offset": 11
        },
        "objects": [
            {
                "code": "S0100-879X1998000900004",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000900004",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000900011",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000900011",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000900012",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000900012",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000900013",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000900013",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000900014",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000900014",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000900015",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000900015",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000900017",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000900017",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000900009",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000900009",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000800005",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000800005",
                "processing_date": "1998-09-21"
            },
            {
                "code": "S0100-879X1998000800001",
                "collection": "scl",
                "doi": "10.1590/S0100-879X1998000800001",
                "processing_date": "1998-09-21"
            }
        ]

    }