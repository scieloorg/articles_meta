===================
/issue/identifiers/
===================

Retorna uma lista de identificadores de fascículos.

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

``GET /api/v1/issue/identifiers/?collection=mex&issn=0036-3634&limit=10``

Resposta:

.. code-block:: json

    {

        "meta": {
            "filter": {
                "collection": "mex",
                "processing_date": {
                    "$lte": "2017-06-27",
                    "$gte": "1500-01-01"
                },
                "code_title": "0036-3634"
            },
            "limit": 10,
            "offset": 0
        },
        "objects": [
            {
                "code": "0036-363420120002",
                "collection": "mex",
                "processing_date": "2012-06-21"
            },
            {
                "code": "0036-363420070008",
                "collection": "mex",
                "processing_date": "2009-08-13"
            },
            {
                "code": "0036-363420050006",
                "collection": "mex",
                "processing_date": "2006-03-21"
            },
            {
                "code": "0036-363420010004",
                "collection": "mex",
                "processing_date": "2001-10-26"
            },
            {
                "code": "0036-363420020007",
                "collection": "mex",
                "processing_date": "2003-08-08"
            },
            {
                "code": "0036-363420130010",
                "collection": "mex",
                "processing_date": "2014-04-03"
            },
            {
                "code": "0036-363420020005",
                "collection": "mex",
                "processing_date": "2003-08-08"
            },
            {
                "code": "0036-363420160004",
                "collection": "mex",
                "processing_date": "2016-07-26"
            },
            {
                "code": "0036-363420070009",
                "collection": "mex",
                "processing_date": "2009-08-07"
            },
            {
                "code": "0036-363420090008",
                "collection": "mex",
                "processing_date": "2009-09-01"
            }
        ]

    }

Próximos 10 registros
=====================

``GET /api/v1/issue/identifiers/?collection=mex&issn=0036-3634&limit=10&offset=11``

Resposta:

.. code-block:: json

    {

        "meta": {
            "filter": {
                "collection": "mex",
                "processing_date": {
                    "$lte": "2017-06-27",
                    "$gte": "1500-01-01"
                },
                "code_title": "0036-3634"
            },
            "limit": 10,
            "offset": 11
        },
        "objects": [
            {
                "code": "0036-363420020001",
                "collection": "mex",
                "processing_date": "2003-08-08"
            },
            {
                "code": "0036-363420060006",
                "collection": "mex",
                "processing_date": "2007-09-04"
            },
            {
                "code": "0036-363420080001",
                "collection": "mex",
                "processing_date": "2009-08-21"
            },
            {
                "code": "0036-363420120001",
                "collection": "mex",
                "processing_date": "2012-06-21"
            },
            {
                "code": "0036-363420120006",
                "collection": "mex",
                "processing_date": "2013-06-24"
            },
            {
                "code": "0036-363420110007",
                "collection": "mex",
                "processing_date": "2011-12-07"
            },
            {
                "code": "0036-363420080005",
                "collection": "mex",
                "processing_date": "2009-09-01"
            },
            {
                "code": "0036-363420030009",
                "collection": "mex",
                "processing_date": "2004-07-14"
            },
            {
                "code": "0036-363420110003",
                "collection": "mex",
                "processing_date": "2011-12-07"
            },
            {
                "code": "0036-363420040001",
                "collection": "mex",
                "processing_date": "2004-06-14"
            }
        ]

    }
