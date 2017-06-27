============
/collection/
============

Retorna os metadados de uma coleção

Parâmetros:

    +------------+-----------------------------------------------------+-------------+
    | Paremetros | Descrição                                           | Obrigatório |
    +============+=====================================================+=============+
    | **code**   | Acrônimo de três letras de coleções SciELO          | sim         |
    +------------+-----------------------------------------------------+-------------+
    | callback   | JSONP callback method                               | não         |
    +------------+-----------------------------------------------------+-------------+

Parâmetros obrigatórios:

    *code* Acrônimo de três letras de coleções SciELO, ex: scl, arg, cub, esp.

--------
Exemplos
--------

``GET /api/v1/collection/?code=scl``

Resposta:

.. code-block:: json

    {

        "original_name": "Brasil",
        "domain": "www.scielo.br",
        "name": {
            "pt": "Brasil",
            "es": "Brasil",
            "en": "Brazil"
        },
        "status": "certified",
        "has_analytics": true,
        "acron": "scl",
        "acron2": "br",
        "code": "scl"

    }