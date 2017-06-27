============
/collection/
============

Retorna os metadados de uma coleção

Parameters:

+------------+-----------------------------------------------------+-------------+
| Paremeter  | Description                                         | Mandatory   |
+============+=====================================================+=============+
| **code**   | Acrônimo de três letras de coleções SciELO          | yes         |
+------------+-----------------------------------------------------+-------------+
| callback   | JSONP callback method                               | No          |
+------------+-----------------------------------------------------+-------------+

Mandatory Parameters:

    *code* Acrônimo de três letras de coleções SciELO, ex: scl, arg, cub, esp.


``GET /api/v1/collection/?code=scl``


Response

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