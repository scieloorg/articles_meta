========================
/collection/identifiers/
========================

Retorna uma lista de coleções com seus metadados e identificadores.

Parâmetros:

    +------------+-----------------------------------------------------+-------------+
    | Paremetros | Descrição                                           | Obrigatório |
    +============+=====================================================+=============+
    | **code**   | Acrônimo de três letras de coleções SciELO          | não         |
    +------------+-----------------------------------------------------+-------------+
    | callback   | JSONP callback method                               | não         |
    +------------+-----------------------------------------------------+-------------+

Parâmetros obrigatórios:

    Não existem parâmetros obrigatórios

--------
Exemplos
--------

``GET /api/v1/collection/identifiers/``

Resposta:

.. code-block:: json

    [

        {
            "name": {
                "pt": "Argentina",
                "es": "Argentina",
                "en": "Argentina"
            },
            "acron2": "ar",
            "original_name": "Argentina",
            "acron": "arg",
            "code": "arg",
            "domain": "www.scielo.org.ar",
            "status": "certified",
            "has_analytics": true
        },
        {
            "name": {
                "pt": "Chile",
                "es": "Chile",
                "en": "Chile"
            },
            "acron2": "cl",
            "original_name": "Chile",
            "acron": "chl",
            "code": "chl",
            "domain": "www.scielo.cl",
            "status": "certified",
            "has_analytics": true
        },
        {
            "name": {
                "pt": "Colombia",
                "es": "Colombia",
                "en": "Colombia"
            },
            "acron2": "co",
            "original_name": "Colombia",
            "acron": "col",
            "code": "col",
            "domain": "www.scielo.org.co",
            "status": "certified",
            "has_analytics": true
        },
       {
            "name": {
                "pt": "Revista de Enfermagem",
                "es": "Revista de Enfermagem",
                "en": "Revista de Enfermagem"
            },
            "acron2": "revenf",
            "original_name": "REVENF",
            "acron": "rve",
            "code": "rve",
            "domain": "www.revenf.bvs.br",
            "status": "independent",
            "has_analytics": true
        }

    ]