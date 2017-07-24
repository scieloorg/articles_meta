=======
/issue/
=======

Retorna os metadados de um fascículo.

Parâmetros:

    +------------+-----------------------------------------------------+-------------+
    | Paremetros | Descrição                                           | Obrigatório |
    +============+=====================================================+=============+
    | **code**   | ID de fascículo do SciELO                           | sim         |
    +------------+-----------------------------------------------------+-------------+
    | collection | Acrônimo de três letras de coleções SciELO          | não         |
    +------------+-----------------------------------------------------+-------------+
    | callback   | JSONP callback method                               | não         |
    +------------+-----------------------------------------------------+-------------+


Parâmetros obrigatórios:

    *code* ID de fascículo do SciELO, ex: 0034-891020130050

--------
Exemplos
--------

``GET /api/v1/issue/?code=0034-891020130050``

Resposta:

.. code-block:: json

    {

        "code": "0034-891020130050",
        "issue": {
            "v200": [
                {
                    "_": "0"
                }
            ],
            "v35": [
                {
                    "_": "0034-8910"
                }
            ],
            "v6": [
                {
                    "_": "287"
                }
            ],
            "v85": [
                {
                    "_": "decs"
                }
            ],
            "v880": [
                {
                    "_": "0034-891020130050"
                }
            ],
            "v992": [
                {
                    "_": "spa"
                }
            ],
            "v43": [
                {
                    "l": "es",
                    "t": "Rev. Saúde Pública",
                    "_": ""
                },
                {
                    "l": "pt",
                    "t": "Rev. Saúde Pública",
                    "_": ""
                },
                {
                    "l": "en",
                    "t": "Rev. Saúde Pública",
                    "_": ""
                }
            ],
            "v65": [
                {
                    "_": "20130000"
                }
            ],
            "v48": [
                {
                    "h": "Sumario",
                    "l": "es",
                    "_": ""
                },
                {
                    "h": "Sumario",
                    "l": "pt",
                    "_": ""
                },
                {
                    "h": "Table of Contents",
                    "l": "en",
                    "_": ""
                }
            ],
            "v230": [
                {
                    "_": "CNPq - Conselho Nacional de Desenvolvimento Científico e Tecnológico"
                }
            ],
            "v42": [
                {
                    "_": "1"
                }
            ],
            "v480": [
                {
                    "_": "CNPq - Conselho Nacional de Desenvolvimento Científico e Tecnológico"
                }
            ],
            "v540": [
                {
                    "l": "en",
                    "t": "<p> </p>",
                    "_": ""
                },
                {
                    "l": "es",
                    "t": "<p> </p>",
                    "_": ""
                },
                {
                    "l": "pt",
                    "t": "<p> </p>",
                    "_": ""
                }
            ],
            "v130": [
                {
                    "_": "Revista de Saúde Pública"
                }
            ],
            "v935": [
                {
                    "_": "0034-8910"
                }
            ],
            "v151": [
                {
                    "_": "Rev. saúde pública"
                }
            ],
            "v117": [
                {
                    "_": "vancouv"
                }
            ],
            "v122": [
                {
                    "_": "10"
                }
            ],
            "v999": [
                {
                    "_": "../bases-work/rsp/rsp"
                }
            ],
            "v706": [
                {
                    "_": "i"
                }
            ],
            "v930": [
                {
                    "_": "rsp"
                }
            ],
            "v541": [
                {
                    "_": "nd"
                }
            ],
            "v36": [
                {
                    "_": "201350"
                }
            ],
            "v32": [
                {
                    "_": "ahead"
                }
            ],
            "v30": [
                {
                    "_": "Rev. Saúde Pública"
                }
            ],
            "v91": [
                {
                    "_": "19980430"
                }
            ]
        },
        "collection": "spa",
        "publication_year": "2013",
        "publication_date": "2013",
        "created_at": "1998-04-30",
        "issue_type": "ahead",
        "title": {
            "v117": [
                {
                    "_": "vancouv"
                }
            ],
            "v950": [
                {
                    "_": "sonia.reis"
                }
            ],
            "v6": [
                {
                    "_": "c"
                }
            ],
            "v51": [
                {
                    "a": "20010801",
                    "b": "C",
                    "_": ""
                }
            ],
            "v85": [
                {
                    "_": "decs"
                }
            ],
            "v880": [
                {
                    "_": "0034-8910"
                }
            ],
            "v940": [
                {
                    "_": "19980430"
                }
            ],
            "v901": [
                {
                    "l": "es",
                    "_": "Publicar y diseminar productos del trabajo científico relevantes para la Salud Pública"
                },
                {
                    "l": "pt",
                    "_": "Publicar e disseminar produtos do trabalho científico que sejam relevantes para a Saúde Pública"
                },
                {
                    "l": "en",
                    "_": "To publish and divulge scientific production on subjects of relevance to Public Health"
                }
            ],
            "v50": [
                {
                    "_": "C"
                }
            ],
            "v301": [
                {
                    "_": "1967"
                }
            ],
            "v100": [
                {
                    "_": "Revista de Saúde Pública"
                }
            ],
            "code": "0034-8910",
            "v935": [
                {
                    "_": "1518-8787"
                }
            ],
            "v943": [
                {
                    "_": "20170530"
                }
            ],
            "v151": [
                {
                    "_": "Rev. saúde pública"
                }
            ],
            "v951": [
                {
                    "_": "sonia.reis"
                }
            ],
            "v310": [
                {
                    "_": "BR"
                }
            ],
            "v941": [
                {
                    "_": "20170530"
                }
            ],
            "v930": [
                {
                    "_": "rsp"
                }
            ],
            "v541": [
                {
                    "_": "BY/4.0"
                }
            ],
            "v440": [
                {
                    "_": "SAUDE COLETIVA"
                },
                {
                    "_": "SAUDE PUBLICA"
                },
                {
                    "_": "MICROBIOLOGIA"
                }
            ],
            "v5": [
                {
                    "_": "S"
                }
            ],
            "v692": [
                {
                    "_": "http://mc04.manuscriptcentral.com/rsp-scielo"
                }
            ],
            "v62": [
                {
                    "_": "Faculdade de Saúde Pública da Universidade de São Paulo"
                }
            ],
            "v63": [
                {
                    "_": "Avenida Dr. Arnaldo, 715, São Paulo, SP, BR, 01246-904, 55 11 3068-0539"
                }
            ],
            "v140": [
                {
                    "_": "CNPq - Conselho Nacional de Desenvolvimento Científico e Tecnológico"
                }
            ],
            "processing_date": "2017-05-30",
            "v240": [
                {
                    "_": "Rev Saude Publica"
                }
            ],
            "v35": [
                {
                    "_": "ONLIN"
                }
            ],
            "collection": "spa",
            "v441": [
                {
                    "_": "Health Sciences"
                }
            ],
            "updated_date": "2016-04-29",
            "v320": [
                {
                    "_": "SP"
                }
            ],
            "v66": [
                {
                    "_": "art"
                }
            ],
            "creted_at": "1998-04-30",
            "v380": [
                {
                    "_": "B"
                }
            ],
            "v992": [
                {
                    "_": "spa"
                }
            ],
            "v64": [
                {
                    "_": "revsp@org.usp.br"
                }
            ],
            "v330": [
                {
                    "_": "CT"
                }
            ],
            "v854": [
                {
                    "_": "Health Policy & Services"
                }
            ],
            "v10": [
                {
                    "_": "br1.1"
                }
            ],
            "v230": [
                {
                    "_": "Journal of Public Health"
                }
            ],
            "v350": [
                {
                    "_": "en"
                },
                {
                    "_": "pt"
                },
                {
                    "_": "es"
                }
            ],
            "v490": [
                {
                    "_": "São Paulo"
                }
            ],
            "v302": [
                {
                    "_": "1"
                }
            ],
            "scimago_id": "22596",
            "v480": [
                {
                    "_": "Faculdade de Saúde Pública da Universidade de São Paulo"
                }
            ],
            "v540": [
                {
                    "l": "en",
                    "t": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"https://i.creativecommons.org/l/by/4.0/80x15.png\" /></a><br />This work is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\">Creative Commons Attribution 4.0 International License</a>.",
                    "_": ""
                },
                {
                    "l": "es",
                    "t": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"https://i.creativecommons.org/l/by/4.0/80x15.png\" /></a><br />This work is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\">Creative Commons Attribution 4.0 International License</a>.",
                    "_": ""
                },
                {
                    "l": "pt",
                    "t": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"https://i.creativecommons.org/l/by/4.0/80x15.png\" /></a><br />This work is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\">Creative Commons Attribution 4.0 International License</a>.",
                    "_": ""
                }
            ],
            "v150": [
                {
                    "_": "Rev. Saúde Pública"
                }
            ],
            "v450": [
                {
                    "_": "CAB-HEALTH"
                },
                {
                    "_": "EMBASE"
                },
                {
                    "_": "POPLINE"
                },
                {
                    "_": "LILACS"
                },
                {
                    "_": "ADSAÚDE"
                },
                {
                    "_": "DOCPAL"
                },
                {
                    "_": "ABSTRACTS ON HYGIENE AND COMMUNICABLE DISEASES"
                },
                {
                    "_": "ABSTRACTS ON ZOOPARASITOLOGY"
                },
                {
                    "_": "BIOLOGICAL ABSTRACTS"
                },
                {
                    "_": "CURRENT CONTENTS/SOCIAL & BEHAVIORAL SCIENCE"
                },
                {
                    "_": "ENTOMOLOGY ABSTRACTS"
                },
                {
                    "_": "EXCERPTA MEDICA"
                },
                {
                    "_": "INDEX MEDICUS"
                },
                {
                    "_": "MICROBIOLOGY ABSTRACTS"
                },
                {
                    "_": "NUTRITION ABSTRACTS AND REVIEWS-SERIESB"
                },
                {
                    "_": "REVIEW MEDICAL VETERINARY ENTOMOLOGY"
                },
                {
                    "_": "SAFETY SCIENCE ABSTRACTS JOURNAL"
                },
                {
                    "_": "SOCIAL SCIENCE CITATION INDEX"
                },
                {
                    "_": "TROPICAL DISEASES BULLETIN"
                },
                {
                    "_": "VETERINARY BULLETIN"
                },
                {
                    "_": "VIROLOGY ABSTRACTS"
                },
                {
                    "_": "ISI"
                },
                {
                    "_": "PUBMED"
                }
            ],
            "updated_at": "2017-06-05",
            "v67": [
                {
                    "_": "na"
                }
            ],
            "v400": [
                {
                    "_": "0034-8910"
                }
            ],
            "v435": [
                {
                    "t": "ONLIN",
                    "_": "1518-8787"
                },
                {
                    "t": "PRINT",
                    "_": "0034-8910"
                }
            ],
            "issns": [
                "0034-8910",
                "1518-8787"
            ],
            "v303": [
                {
                    "_": "1"
                }
            ],
            "v421": [
                {
                    "_": "Rev Saude Publica"
                }
            ],
            "v942": [
                {
                    "_": "19980430"
                }
            ],
            "v20": [
                {
                    "_": "068227-6"
                }
            ],
            "v68": [
                {
                    "_": "rsp"
                }
            ]
        },
        "code_title": [
            "0034-8910",
            "1518-8787"
        ],
        "_shard_id": "e8397e92f8794ad2b6a902a1ea1e2a35",
        "processing_date": "1998-04-30"

    }