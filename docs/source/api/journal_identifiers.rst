=====================
/journal/identifiers/
=====================

Retorna uma lista de identificadores de periódicos.

Parâmetros:

    +------------+-----------------------------------------------------+-------------+
    | Paremetros | Descrição                                           | Obrigatório |
    +============+=====================================================+=============+
    | collection | Acrônimo de três letras de coleções SciELO          | não         |
    +------------+-----------------------------------------------------+-------------+
    | limit      | Total de registros por requisição, máximo 1000.     | não         |
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

``GET /api/v1/journal/identifiers/?collection=scl&limit=10``

Resposta:

.. code-block:: json

    {
        "meta": {
            "filter": {
                "collection": "scl"
            },
            "offset": 0,
            "limit": 10
        },
        "objects": [
            {
                "code": "1678-8621",
                "collection": "scl",
                "processing_date": "2017-06-08"
            },
            {
                "code": "0365-0596",
                "collection": "scl",
                "processing_date": "2016-11-23"
            },
            {
                "code": "2236-9996",
                "collection": "scl",
                "processing_date": "2017-02-08"
            },
            {
                "code": "0366-6913",
                "collection": "scl",
                "processing_date": "2016-11-23"
            },
            {
                "code": "1678-5320",
                "collection": "scl",
                "processing_date": "2016-11-23"
            },
            {
                "code": "0102-3306",
                "collection": "scl",
                "processing_date": "2017-02-08"
            },
            {
                "code": "1807-8621",
                "collection": "scl",
                "processing_date": "2016-11-23"
            },
            {
                "code": "1807-8672",
                "collection": "scl",
                "processing_date": "2016-11-23"
            },
            {
                "code": "1981-5794",
                "collection": "scl",
                "processing_date": "2016-11-23"
            },
            {
                "code": "0103-636X",
                "collection": "scl",
                "processing_date": "2017-04-25"
            }
        ]
    }

Próximos 10 registros
=====================

``GET /api/v1/journal/identifiers/?collection=scl&limit=10&offset=11``

Resposta:

.. code-block:: json

    {

        "meta": {
            "filter": {
                "collection": "scl"
            },
            "limit": 10,
            "offset": 11
        },
        "objects": [
            {
                "code": "0104-7760",
                "collection": "scl",
                "processing_date": "2016-11-23"
            },
            {
                "code": "1980-5764",
                "collection": "scl",
                "processing_date": "2017-02-22"
            },
            {
                "code": "2175-6236",
                "collection": "scl",
                "processing_date": "2016-12-13"
            },
            {
                "code": "1983-2117",
                "collection": "scl",
                "processing_date": "2017-05-16"
            },
            {
                "code": "0103-166X",
                "collection": "scl",
                "processing_date": "2016-07-08"
            },
            {
                "code": "2236-3459",
                "collection": "scl",
                "processing_date": "2016-12-13"
            },
            {
                "code": "2179-6491",
                "collection": "scl",
                "processing_date": "2013-07-03"
            },
            {
                "code": "2175-9146",
                "collection": "scl",
                "processing_date": "2017-01-06"
            },
            {
                "code": "0100-7386",
                "collection": "scl",
                "processing_date": "2014-01-14"
            },
            {
                "code": "0100-6045",
                "collection": "scl",
                "processing_date": "2017-05-05"
            }
        ]

    }
