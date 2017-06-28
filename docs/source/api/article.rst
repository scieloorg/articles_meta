=========
/article/
=========

Retorna os metadados de um documento (artigo).

Parâmetros:

    +------------+-----------------------------------------------------+-------------+
    | Paremetros | Descrição                                           | Obrigatório |
    +============+=====================================================+=============+
    | **code**   | ID de documentos do SciELO (PID)                    | sim         |
    +------------+-----------------------------------------------------+-------------+
    | collection | Acrônimo de três letras de coleções SciELO          | não         |
    +------------+-----------------------------------------------------+-------------+
    | format     | Formato de entrega dos metadados                    | não         |
    +------------+-----------------------------------------------------+-------------+
    | body       | Boolean (true, false)                               | não         |
    +------------+-----------------------------------------------------+-------------+
    | callback   | JSONP callback method                               | não         |
    +------------+-----------------------------------------------------+-------------+


Parâmetros obrigatórios:

    *code* PID de documento do SciELO, ex: S0100-879X1998000800011

--------
Exemplos
--------

Formato Padrão
==============

``GET /api/v1/article/?code=S0100-879X1998000800011``

Resposta:

.. code-block:: json

    {

        "version": "html",
        "validated_scielo": "False",
        "section": {
            "en": "Physiology and biophysics"
        },
        "sent_wos": "False",
        "doi": "10.1590/S0100-879X1998000800011",
        "applicable": "True",
        "created_at": "1998-09-21",
        "title": {
            "v950": [
                {
                    "_": "MRB"
                }
            ],
            "v350": [
                {
                    "_": "en"
                }
            ],
            "v117": [
                {
                    "_": "other"
                }
            ],
            "v35": [
                {
                    "_": "ONLIN"
                }
            ],
            "v901": [
                {
                    "l": "es",
                    "_": "Publicar los resultados de investigaciones originales que realicen aportes significativos en el área de las ciencias médicas y biológicas"
                },
                {
                    "l": "pt",
                    "_": "Publicar resultados de pesquisas originais que contribuam significativamente para o conhecimento no campo das ciências médicas e biológicas"
                },
                {
                    "l": "en",
                    "_": "To publish the results of original research which contribute significantly to knowledge in medical and biological sciences"
                }
            ],
            "v691": [
                {
                    "_": "100000000000000000000000"
                }
            ],
            "v66": [
                {
                    "_": "art"
                }
            ],
            "v68": [
                {
                    "_": "bjmbr"
                }
            ],
            "v6": [
                {
                    "_": "ms"
                }
            ],
            "v303": [
                {
                    "_": "1"
                }
            ],
            "v610": [
                {
                    "_": "Revista brasileira de pesquisas médicas e biológicas"
                }
            ],
            "v940": [
                {
                    "_": "19970424"
                }
            ],
            "scimago_id": "28675",
            "v851": [
                {
                    "_": "SCIE"
                }
            ],
            "v854": [
                {
                    "_": "BIOLOGY"
                },
                {
                    "_": "MEDICINE, RESEARCH & EXPERIMENTAL"
                }
            ],
            "v320": [
                {
                    "_": "SP"
                }
            ],
            "v690": [
                {
                    "_": "www.scielo.br"
                }
            ],
            "v302": [
                {
                    "_": "14"
                }
            ],
            "v150": [
                {
                    "_": "Braz J Med Biol Res"
                }
            ],
            "issns": [
                "1414-431X",
                "0100-879X"
            ],
            "v435": [
                {
                    "t": "ONLIN",
                    "_": "1414-431X"
                }
            ],
            "v230": [
                {
                    "_": "Revista brasileira de pesquisas médicas e biológicas"
                }
            ],
            "creted_at": "1997-04-24",
            "v942": [
                {
                    "_": "19970424"
                }
            ],
            "v63": [
                {
                    "_": "Av. Bandeirantes, 3900"
                },
                {
                    "_": "14049-900 Ribeirão Preto SP Brazil"
                },
                {
                    "_": "Tel. / Fax: +55 16 3315-9120"
                }
            ],
            "v541": [
                {
                    "_": "BY"
                }
            ],
            "v992": [
                {
                    "_": "scl"
                }
            ],
            "collection": "scl",
            "code": "0100-879X",
            "v880": [
                {
                    "_": "0100-879X"
                }
            ],
            "v450": [
                {
                    "_": "Current contents. Life sciences"
                },
                {
                    "_": "SciSearch"
                },
                {
                    "_": "Science citation index : an international interdisciplinary index to the literature"
                },
                {
                    "_": "Research Alert"
                },
                {
                    "_": "Index medicus (Washington. 1879)"
                },
                {
                    "_": "Chemical Abstracts Service"
                },
                {
                    "_": "Biological Abstracts"
                },
                {
                    "_": "Biosciences Information Service"
                },
                {
                    "_": "Excerpta Medica"
                },
                {
                    "_": "Index Medicus Latino-Americano"
                },
                {
                    "_": "ISI"
                },
                {
                    "_": "LILACS"
                },
                {
                    "_": "PubMed"
                }
            ],
            "v421": [
                {
                    "_": "Braz J Med Biol Res"
                }
            ],
            "v692": [
                {
                    "_": "http://mc04.manuscriptcentral.com/bjmbr-scielo"
                }
            ],
            "v62": [
                {
                    "_": "Brazilian Journal of Medical and Biological Research"
                }
            ],
            "v951": [
                {
                    "_": "MRB"
                }
            ],
            "v340": [
                {
                    "_": "B"
                }
            ],
            "v85": [
                {
                    "_": "nd"
                }
            ],
            "v301": [
                {
                    "_": "1981"
                }
            ],
            "v30": [
                {
                    "_": "fbpe-3318"
                }
            ],
            "v51": [
                {
                    "a": "19970424",
                    "b": "C",
                    "_": ""
                }
            ],
            "v930": [
                {
                    "_": "BJMBR"
                }
            ],
            "v310": [
                {
                    "_": "BR"
                }
            ],
            "v67": [
                {
                    "_": "na"
                }
            ],
            "v380": [
                {
                    "_": "M"
                }
            ],
            "v50": [
                {
                    "_": "C"
                }
            ],
            "v360": [
                {
                    "_": "en"
                }
            ],
            "v480": [
                {
                    "_": "Associação Brasileira de Divulgação Científica"
                }
            ],
            "updated_date": "2016-06-14",
            "v20": [
                {
                    "_": "016281-7"
                }
            ],
            "v440": [
                {
                    "_": "MEDICINA"
                },
                {
                    "_": "BIOLOGIA GERAL"
                }
            ],
            "v151": [
                {
                    "_": "Braz. j. med. biol. res"
                }
            ],
            "v5": [
                {
                    "_": "S"
                }
            ],
            "v100": [
                {
                    "_": "Brazilian Journal of Medical and Biological Research"
                }
            ],
            "v69": [
                {
                    "_": "http://www.bjournal.com.br"
                }
            ],
            "v65": [
                {
                    "_": "<p align=\"center\"><img src=\"http:/fbpe/img/revistas/bjmbr/barrinha.jpg\" width=\"599\" height=\"10\">"
                }
            ],
            "v420": [
                {
                    "_": "BOF"
                }
            ],
            "v490": [
                {
                    "_": "Ribeirão Preto"
                }
            ],
            "v699": [
                {
                    "_": "continuous"
                }
            ],
            "v10": [
                {
                    "_": "bjmbr"
                }
            ],
            "v330": [
                {
                    "_": "CT"
                }
            ],
            "v900": [
                {
                    "_": "ISSN impresso: 0100-879X"
                }
            ],
            "v430": [
                {
                    "_": "QH W20.5"
                }
            ],
            "updated_at": "2017-05-20",
            "v64": [
                {
                    "_": "bjournal@terra.com.br"
                }
            ],
            "v935": [
                {
                    "_": "1414-431X"
                }
            ],
            "v441": [
                {
                    "_": "Biological Sciences"
                },
                {
                    "_": "Health Sciences"
                }
            ],
            "v943": [
                {
                    "_": "20170516"
                }
            ],
            "processing_date": "2017-05-16",
            "v400": [
                {
                    "_": "0100-879X"
                }
            ],
            "v941": [
                {
                    "_": "20170516"
                }
            ]
        },
        "citations": [
            {
                "v30": [
                    {
                        "_": "Journal of Nutrition"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0022-3166"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "The evaluation of the scientific evidence for a relationship between calcium and hypertension"
                    }
                ],
                "v801": [
                    {
                        "_": "Journal of Nutrition"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "1"
                    }
                ],
                "v118": [
                    {
                        "_": "1"
                    }
                ],
                "v700": [
                    {
                        "_": "46"
                    }
                ],
                "v65": [
                    {
                        "_": "19950000"
                    }
                ],
                "v10": [
                    {
                        "n": "P",
                        "s": "Hamet",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100001"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1995"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "311s-400s"
                    }
                ],
                "mixed": "<p>1. Hamet P (1995). The evaluation of the scientific evidence for a relationship between calcium and hypertension. <i>Journal of Nutrition</i>, 125: 311s-400s. </P>",
                "v31": [
                    {
                        "_": "125"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Science"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0036-8075"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Blood pressure and nutrient intake in the United States"
                    }
                ],
                "v801": [
                    {
                        "_": "Science"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "2"
                    }
                ],
                "v118": [
                    {
                        "_": "2"
                    }
                ],
                "v700": [
                    {
                        "_": "47"
                    }
                ],
                "v65": [
                    {
                        "_": "19840000"
                    }
                ],
                "v10": [
                    {
                        "n": "DA",
                        "s": "McCarron",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "DC",
                        "s": "Morris",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "JH",
                        "s": "Henry",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "JL",
                        "s": "Santon",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100002"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1984"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "1392-1398"
                    }
                ],
                "mixed": "<p>2. McCarron DA, Morris DC, Henry JH & Santon JL (1984). Blood pressure and nutrient intake in the United States. <i>Science,</i> 224: 1392-1398. </P>",
                "v31": [
                    {
                        "_": "224"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Journal of the American Medical Association"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0098-7484"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Reduction of blood pressure with calcium supplementation in young adults"
                    }
                ],
                "v801": [
                    {
                        "_": "Journal of the American Medical Association"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "3"
                    }
                ],
                "v118": [
                    {
                        "_": "3"
                    }
                ],
                "v700": [
                    {
                        "_": "48"
                    }
                ],
                "v65": [
                    {
                        "_": "19830000"
                    }
                ],
                "v10": [
                    {
                        "n": "JM",
                        "s": "Belizan",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "J",
                        "s": "Vilar",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "O",
                        "s": "Pineda",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "AE",
                        "s": "Gonzalez",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "E",
                        "s": "Sainz",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "G",
                        "s": "Garrera",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "R",
                        "s": "Sibrian",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100003"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1983"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "1161-1165"
                    }
                ],
                "mixed": "<p>3. Belizan JM, Vilar J, Pineda O, Gonzalez AE, Sainz E, Garrera G & Sibrian R (1983). Reduction of blood pressure with calcium supplementation in young adults. <i>Journal of the American Medical Association,</i> 249: 1161-1165. </P>",
                "v31": [
                    {
                        "_": "249"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Journal of Clinical Investigation"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0021-9738"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Blood pressure development of the spontaneously hypertensive rat after concurrent manipulations of dietary calcium and sodium"
                    }
                ],
                "v801": [
                    {
                        "_": "Journal of Clinical Investigation"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "4"
                    }
                ],
                "v118": [
                    {
                        "_": "4"
                    }
                ],
                "v700": [
                    {
                        "_": "49"
                    }
                ],
                "v65": [
                    {
                        "_": "19850000"
                    }
                ],
                "v10": [
                    {
                        "n": "DA",
                        "s": "McCarron",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "PA",
                        "s": "Lucas",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "RJ",
                        "s": "Sheidman",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "B",
                        "s": "LaCour",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "D",
                        "s": "Tilman",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100004"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1985"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "1147-1154"
                    }
                ],
                "mixed": "<p>4. McCarron DA, Lucas PA, Sheidman RJ, LaCour B & Tilman D (1985). Blood pressure development of the spontaneously hypertensive rat after concurrent manipulations of dietary calcium and sodium. <i>Journal of Clinical Investigation,</i> 76: 1147-1154. </P>",
                "v31": [
                    {
                        "_": "76"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "American Journal of Clinical Nutrition"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0002-9165"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Effects on blood pressure of calcium supplementation of women"
                    }
                ],
                "v801": [
                    {
                        "_": "American Journal of Clinical Nutrition"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "5"
                    }
                ],
                "v118": [
                    {
                        "_": "5"
                    }
                ],
                "v700": [
                    {
                        "_": "50"
                    }
                ],
                "v65": [
                    {
                        "_": "19850000"
                    }
                ],
                "v10": [
                    {
                        "n": "NE",
                        "s": "Johnson",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "EL",
                        "s": "Smith",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "JL",
                        "s": "Freudenhaim",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100005"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1985"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "12-17"
                    }
                ],
                "mixed": "<p>5. Johnson NE, Smith EL & Freudenhaim JL (1985). Effects on blood pressure of calcium supplementation of women. <i>American Journal of Clinical Nutrition,</i> 42: 12-17. </P>",
                "v31": [
                    {
                        "_": "42"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Annals of Internal Medicine"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0003-4819"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Blood pressure responses to oral calcium in persons with mild to moderate hypertension"
                    }
                ],
                "v801": [
                    {
                        "_": "Annals of Internal Medicine"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "6"
                    }
                ],
                "v118": [
                    {
                        "_": "6"
                    }
                ],
                "v700": [
                    {
                        "_": "51"
                    }
                ],
                "v65": [
                    {
                        "_": "19850000"
                    }
                ],
                "v10": [
                    {
                        "n": "DA",
                        "s": "McCarron",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "DC",
                        "s": "Morris",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100006"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1985"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "6825-6831"
                    }
                ],
                "mixed": "<p>6. McCarron DA & Morris DC (1985). Blood pressure responses to oral calcium in persons with mild to moderate hypertension. <i>Annals of Internal Medicine, </i>103: 6825-6831. </P>",
                "v31": [
                    {
                        "_": "103"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Science"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0036-8075"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Hypertension and calcium"
                    }
                ],
                "v801": [
                    {
                        "_": "Science"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "7"
                    }
                ],
                "v118": [
                    {
                        "_": "7"
                    }
                ],
                "v700": [
                    {
                        "_": "52"
                    }
                ],
                "v65": [
                    {
                        "_": "19840000"
                    }
                ],
                "v10": [
                    {
                        "n": "M",
                        "s": "Feinleib",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "C",
                        "s": "Lenfant",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "SA",
                        "s": "Miller",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100007"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1984"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "384-386"
                    }
                ],
                "mixed": "<p>7. Feinleib M, Lenfant C & Miller SA (1984). Hypertension and calcium. <i>Science,</i> 226: 384-386. </P>",
                "v31": [
                    {
                        "_": "226"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Hypertension"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0194-911X"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Dietary calcium and blood pressure in National Health and Nutrition Examination Surveys I and II"
                    }
                ],
                "v801": [
                    {
                        "_": "Hypertension"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "8"
                    }
                ],
                "v118": [
                    {
                        "_": "8"
                    }
                ],
                "v700": [
                    {
                        "_": "53"
                    }
                ],
                "v65": [
                    {
                        "_": "19860000"
                    }
                ],
                "v10": [
                    {
                        "n": "C",
                        "s": "Sempos",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "R",
                        "s": "Cooper",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "MG",
                        "s": "Kovar",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "C",
                        "s": "Johnson",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "T",
                        "s": "Drizd",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "E",
                        "s": "Yetley",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100008"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1986"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "1067-1074"
                    }
                ],
                "mixed": "<p>8. Sempos C, Cooper R, Kovar MG, Johnson C, Drizd T & Yetley E (1986). Dietary calcium and blood pressure in National Health and Nutrition Examination Surveys I and II. <i>Hypertension,</i> 8: 1067-1074. </P>",
                "v31": [
                    {
                        "_": "8"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "American Journal of the Medical Sciences"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Stress modulation by electrolytes in salt sensitive spontaneously hypertensive rats"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "9"
                    }
                ],
                "v118": [
                    {
                        "_": "9"
                    }
                ],
                "v700": [
                    {
                        "_": "54"
                    }
                ],
                "v65": [
                    {
                        "_": "19940000"
                    }
                ],
                "v10": [
                    {
                        "n": "P",
                        "s": "Dumas",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "J",
                        "s": "Tremblay",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "P",
                        "s": "Hamet",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100009"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1994"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "S130-S137"
                    }
                ],
                "mixed": "<p>9. Dumas P, Tremblay J & Hamet P (1994). Stress modulation by electrolytes in salt sensitive spontaneously hypertensive rats. <i>American Journal of the Medical Sciences,</i> 307 (Suppl 1): S130-S137. </P>",
                "v31": [
                    {
                        "_": "307"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v32": [
                    {
                        "n": "1",
                        "_": ""
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "American Journal of Hypertension"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0895-7061"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Mesenteric artery contractile properties during dietary calcium manipulation in spontaneously hypertensive and Wistar Kyoto normotensive rats"
                    }
                ],
                "v801": [
                    {
                        "_": "American Journal of Hypertension"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "10"
                    }
                ],
                "v118": [
                    {
                        "_": "10"
                    }
                ],
                "v700": [
                    {
                        "_": "55"
                    }
                ],
                "v65": [
                    {
                        "_": "19890000"
                    }
                ],
                "v10": [
                    {
                        "n": "RD",
                        "s": "Bukoski",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "H",
                        "s": "Xue",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "DA",
                        "s": "McCarron",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100010"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1989"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "440-448"
                    }
                ],
                "mixed": "<p>10. Bukoski RD, Xue H & McCarron DA (1989). Mesenteric artery contractile properties during dietary calcium manipulation in spontaneously hypertensive and Wistar Kyoto normotensive rats. <i>American Journal of Hypertension,</i> 2: 440-448. </P>",
                "v31": [
                    {
                        "_": "2"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Journal of Nutrition"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0022-3166"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Dietary calcium modifies concentrations of lead and other metals and renal calbindin in rats"
                    }
                ],
                "v801": [
                    {
                        "_": "Journal of Nutrition"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "11"
                    }
                ],
                "v118": [
                    {
                        "_": "11"
                    }
                ],
                "v700": [
                    {
                        "_": "56"
                    }
                ],
                "v65": [
                    {
                        "_": "19920000"
                    }
                ],
                "v10": [
                    {
                        "n": "DJ",
                        "s": "Bogden",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "SB",
                        "s": "Gertner",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "S",
                        "s": "Christakos",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "WF",
                        "s": "Kemp",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "Z",
                        "s": "Yang",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "RS",
                        "s": "Katz",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "C",
                        "s": "Chu",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100011"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1992"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "1351-1360"
                    }
                ],
                "mixed": "<p>11. Bogden DJ, Gertner SB, Christakos S, Kemp WF, Yang Z, Katz RS & Chu C (1992). Dietary calcium modifies concentrations of lead and other metals and renal calbindin in rats. <i>Journal of Nutrition,</i> 122: 1351-1360. </P>",
                "v31": [
                    {
                        "_": "122"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Nutrition Reviews"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0271-5317"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "A review of calcium preparation"
                    }
                ],
                "v801": [
                    {
                        "_": "Nutrition Reviews"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "12"
                    }
                ],
                "v118": [
                    {
                        "_": "12"
                    }
                ],
                "v700": [
                    {
                        "_": "57"
                    }
                ],
                "v65": [
                    {
                        "_": "19940000"
                    }
                ],
                "v10": [
                    {
                        "n": "DI",
                        "s": "Levenson",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "RS",
                        "s": "Bockman",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100012"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1994"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "221-232"
                    }
                ],
                "mixed": "<p>12. Levenson DI & Bockman RS (1994). A review of calcium preparation. <i>Nutrition Reviews,</i> 52: 221-232. </P>",
                "v31": [
                    {
                        "_": "52"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v66": [
                    {
                        "e": "NC",
                        "_": "Cary"
                    }
                ],
                "v65": [
                    {
                        "_": "19850000"
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "13"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100013"
                    }
                ],
                "v18": [
                    {
                        "l": "en",
                        "_": "Guide for Personal Computers. Version 6"
                    }
                ],
                "v64": [
                    {
                        "_": "1985"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "183-260"
                    }
                ],
                "v62": [
                    {
                        "_": "SAS Circle"
                    }
                ],
                "v118": [
                    {
                        "_": "13"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v700": [
                    {
                        "_": "58"
                    }
                ],
                "v17": [
                    {
                        "d": "SAS Institute Inc.",
                        "_": "SAS/SAT"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Journal of Nutrition"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0022-3166"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Dietary calcium and lead interact to modify maternal blood pressure, erythropoiesis and fetal and neonatal growth in rats during pregnancy and lactation"
                    }
                ],
                "v801": [
                    {
                        "_": "Journal of Nutrition"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "14"
                    }
                ],
                "v118": [
                    {
                        "_": "14"
                    }
                ],
                "v700": [
                    {
                        "_": "59"
                    }
                ],
                "v65": [
                    {
                        "_": "19950000"
                    }
                ],
                "v10": [
                    {
                        "n": "DJ",
                        "s": "Bogden",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "WF",
                        "s": "Kemp",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "S",
                        "s": "Hans",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "M",
                        "s": "Murphy",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "M",
                        "s": "Fraiman",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "D",
                        "s": "Czerniach",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "JC",
                        "s": "Flynn",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "LM",
                        "s": "Banua",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "A",
                        "s": "Scimone",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "L",
                        "s": "Castrovilly",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "BS",
                        "s": "Gertner",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100014"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1995"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "990-1002"
                    }
                ],
                "mixed": "<p>14. Bogden DJ, Kemp WF, Hans S, Murphy M, Fraiman M, Czerniach D, Flynn JC, Banua LM, Scimone A, Castrovilly L & Gertner BS (1995). Dietary calcium and lead interact to modify maternal blood pressure, erythropoiesis and fetal and neonatal growth in rats during pregnancy and lactation. <i>Journal of Nutrition,</i> 125: 990-1002. </P>",
                "v31": [
                    {
                        "_": "125"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v66": [
                    {
                        "e": "DC",
                        "_": "Washington"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Nutrient requirements of the laboratory rat."
                    }
                ],
                "v11": [
                    {
                        "_": "National Academy of Sciences"
                    },
                    {
                        "_": "National Research Council"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "15"
                    }
                ],
                "v18": [
                    {
                        "l": "en",
                        "_": "Nutrient Requirements of Laboratory Animals."
                    }
                ],
                "v118": [
                    {
                        "_": "15"
                    }
                ],
                "v700": [
                    {
                        "_": "60"
                    }
                ],
                "v65": [
                    {
                        "_": "19780000"
                    }
                ],
                "v63": [
                    {
                        "_": "3rd edn."
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100015"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1978"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "mixed": "<p>15. National Academy of Sciences/National Research Council (1978). Nutrient requirements of the laboratory rat. In: <i>Nutrient Requirements of Laboratory Animals.</i> 3rd edn. National Academy Press, Washington, DC. </P>",
                "v62": [
                    {
                        "_": "National Academy Press"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Hypertension"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0194-911X"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Calcium, magnesium and phosphorus balance in human and experimental hypertension"
                    }
                ],
                "v801": [
                    {
                        "_": "Hypertension"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "16"
                    }
                ],
                "v118": [
                    {
                        "_": "16"
                    }
                ],
                "v700": [
                    {
                        "_": "61"
                    }
                ],
                "v65": [
                    {
                        "_": "19820000"
                    }
                ],
                "v10": [
                    {
                        "n": "DA",
                        "s": "McCarron",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100016"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1982"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v31": [
                    {
                        "_": "4"
                    }
                ],
                "v14": [
                    {
                        "_": "27-33"
                    }
                ],
                "mixed": "<p>16. McCarron DA (1982). Calcium, magnesium and phosphorus balance in human and experimental hypertension.<i> Hypertension,</i> 4 (Suppl III): 27-33. </P>",
                "v32": [
                    {
                        "n": "III",
                        "_": ""
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Life Sciences"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0024-3205"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Blood pressure and calcium balance in the Wistar Kyoto rat"
                    }
                ],
                "v801": [
                    {
                        "_": "Life Sciences"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "17"
                    }
                ],
                "v118": [
                    {
                        "_": "17"
                    }
                ],
                "v700": [
                    {
                        "_": "62"
                    }
                ],
                "v65": [
                    {
                        "_": "19820000"
                    }
                ],
                "v10": [
                    {
                        "n": "DA",
                        "s": "McCarron",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100017"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1982"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "683-689"
                    }
                ],
                "mixed": "<p>17. McCarron DA (1982). Blood pressure and calcium balance in the Wistar Kyoto rat. <i>Life</i> <i>Sciences</i>, 30: 683-689. </P>",
                "v31": [
                    {
                        "_": "30"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Metabolism"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0026-0495"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Possible involvement of atrial natriuretic factor in the antihypertensive action of a high calcium diet in spontaneously hypertensive and Wistar Kyoto rats"
                    }
                ],
                "v801": [
                    {
                        "_": "Metabolism"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "18"
                    }
                ],
                "v118": [
                    {
                        "_": "18"
                    }
                ],
                "v700": [
                    {
                        "_": "63"
                    }
                ],
                "v65": [
                    {
                        "_": "19890000"
                    }
                ],
                "v10": [
                    {
                        "n": "M",
                        "s": "Kohno",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "KI",
                        "s": "Murakawa",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "K",
                        "s": "Yassunari",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "K",
                        "s": "Yokokawa",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "N",
                        "s": "Kurihara",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "T",
                        "s": "Takeda",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100018"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1989"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "997-1004"
                    }
                ],
                "mixed": "<p>18. Kohno M, Murakawa KI, Yassunari K, Yokokawa K, Kurihara N & Takeda T (1989). Possible involvement of atrial natriuretic factor in the antihypertensive action of a high calcium diet in spontaneously hypertensive and Wistar Kyoto rats. <i>Metabolism,</i> 38: 997-1004. </P>",
                "v31": [
                    {
                        "_": "38"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "Journal of the American College of Nutrition"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0735-1097"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "Effect of increased dietary calcium on the development of reduced renal mass saline hypertension in rats"
                    }
                ],
                "v801": [
                    {
                        "_": "Journal of the American College of Nutrition"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "19"
                    }
                ],
                "v118": [
                    {
                        "_": "19"
                    }
                ],
                "v700": [
                    {
                        "_": "64"
                    }
                ],
                "v65": [
                    {
                        "_": "19900000"
                    }
                ],
                "v10": [
                    {
                        "n": "MB",
                        "s": "Pamnani",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "S",
                        "s": "Chen",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "HJ",
                        "s": "Bryant",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "JF",
                        "s": "Schooley",
                        "r": "ND",
                        "_": ""
                    },
                    {
                        "n": "FJ",
                        "s": "Haddy",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100019"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1990"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "35-43"
                    }
                ],
                "mixed": "<p>19. Pamnani MB, Chen S, Bryant HJ, Schooley JF & Haddy FJ (1990). Effect of increased dietary calcium on the development of reduced renal mass saline hypertension in rats. <i>Journal of the American College of Nutrition,</i> 9: 35-43. </P>",
                "v31": [
                    {
                        "_": "9"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            },
            {
                "v30": [
                    {
                        "_": "American Journal of Hypertension"
                    }
                ],
                "v706": [
                    {
                        "_": "c"
                    }
                ],
                "v35": [
                    {
                        "_": "0895-7061"
                    }
                ],
                "v882": [
                    {
                        "n": "8",
                        "v": "31",
                        "_": ""
                    }
                ],
                "v12": [
                    {
                        "l": "en",
                        "_": "The intracellular calcium-force relationship in vascular smooth muscle: time and stimulus dependent dissociation"
                    }
                ],
                "v801": [
                    {
                        "_": "American Journal of Hypertension"
                    }
                ],
                "v705": [
                    {
                        "_": "S"
                    }
                ],
                "v701": [
                    {
                        "_": "20"
                    }
                ],
                "v118": [
                    {
                        "_": "20"
                    }
                ],
                "v700": [
                    {
                        "_": "65"
                    }
                ],
                "v65": [
                    {
                        "_": "19900000"
                    }
                ],
                "v10": [
                    {
                        "n": "H",
                        "s": "Karaki",
                        "r": "ND",
                        "_": ""
                    }
                ],
                "v702": [
                    {
                        "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v880": [
                    {
                        "_": "S0100-879X199800080001100020"
                    }
                ],
                "v865": [
                    {
                        "_": "19980800"
                    }
                ],
                "v64": [
                    {
                        "_": "1990"
                    }
                ],
                "v936": [
                    {
                        "y": "1998",
                        "i": "0100-879X",
                        "o": "8",
                        "_": ""
                    }
                ],
                "v14": [
                    {
                        "_": "253s-256s"
                    }
                ],
                "mixed": "<p>20. Karaki H (1990). The intracellular calcium-force relationship in vascular smooth muscle: time and stimulus dependent dissociation. <i>American Journal of Hypertension,</i> 3: 253s-256s. </P>",
                "v31": [
                    {
                        "_": "3"
                    }
                ],
                "v4": [
                    {
                        "_": "v31n8"
                    }
                ],
                "v2": [
                    {
                        "_": "S0100-879X(98)03100811"
                    }
                ]
            }
        ],
        "_shard_id": "c8347cf5adb1419c84ece9fee12b7dbe",
        "license": "by/4.0",
        "validated_wos": "False",
        "publication_year": "1998",
        "fulltexts": {
            "pdf": {
                "en": "http://www.scielo.br/pdf/bjmbr/v31n8/2845c.pdf"
            },
            "html": {
                "en": "http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0100-879X1998000800011&tlng=en"
            }
        },
        "document_type": "rapid-communication",
        "issue": {
            "issue_type": "regular",
            "processing_date": "1998-08-26",
            "created_at": "1998-08-26",
            "code": "0100-879X19980008",
            "_shard_id": "60dfb4f09eaf4ea0b2e266d1a02769d0",
            "collection": "scl",
            "issue": {
                "v91": [
                    {
                        "_": "19980826"
                    }
                ],
                "v30": [
                    {
                        "_": "Braz J Med Biol Res"
                    }
                ],
                "v706": [
                    {
                        "_": "i"
                    }
                ],
                "v35": [
                    {
                        "_": "0100-879X"
                    }
                ],
                "v130": [
                    {
                        "_": "Brazilian Journal of Medical and Biological Research"
                    }
                ],
                "v930": [
                    {
                        "_": "BJMBR"
                    }
                ],
                "v701": [
                    {
                        "_": "1"
                    }
                ],
                "v6": [
                    {
                        "_": "020"
                    }
                ],
                "v43": [
                    {
                        "l": "pt",
                        "c": "Ribeirão Preto",
                        "v": "v. 31",
                        "n": "n. 8",
                        "a": "1998",
                        "_": "",
                        "m": "Ago.",
                        "t": "Braz J Med Biol Res"
                    },
                    {
                        "l": "en",
                        "c": "Ribeirão Preto",
                        "v": "vol. 31",
                        "n": "no. 8",
                        "a": "1998",
                        "_": "",
                        "m": "Aug.",
                        "t": "Braz J Med Biol Res"
                    },
                    {
                        "l": "es",
                        "c": "Ribeirão Preto",
                        "v": "v. 31",
                        "n": "n. 8",
                        "a": "1998",
                        "_": "",
                        "m": "Ago.",
                        "t": "Braz J Med Biol Res"
                    }
                ],
                "v700": [
                    {
                        "_": "0"
                    }
                ],
                "v230": [
                    {
                        "_": "Revista brasileira de pesquisas médicas e biológicas"
                    }
                ],
                "v65": [
                    {
                        "_": "19980800"
                    }
                ],
                "v122": [
                    {
                        "_": "11"
                    }
                ],
                "v36": [
                    {
                        "_": "19988"
                    }
                ],
                "v992": [
                    {
                        "_": "scl"
                    }
                ],
                "v49": [
                    {
                        "l": "en",
                        "c": "BJMBR090",
                        "t": "Review",
                        "_": ""
                    },
                    {
                        "l": "en",
                        "c": "BJMBR010",
                        "t": "Biochemistry and molecular biology",
                        "_": ""
                    },
                    {
                        "l": "en",
                        "c": "BJMBR040",
                        "t": "Experimental biology",
                        "_": ""
                    },
                    {
                        "l": "en",
                        "c": "BJMBR050",
                        "t": "Immunology",
                        "_": ""
                    },
                    {
                        "l": "en",
                        "c": "BJMBR060",
                        "t": "Neurosciences and behavior",
                        "_": ""
                    },
                    {
                        "l": "en",
                        "c": "BJMBR070",
                        "t": "Pharmacology",
                        "_": ""
                    },
                    {
                        "l": "en",
                        "c": "BJMBR080",
                        "t": "Physiology and biophysics",
                        "_": ""
                    }
                ],
                "v880": [
                    {
                        "_": "0100-879X19980008"
                    }
                ],
                "v64": [
                    {
                        "a": "1998",
                        "m": "08",
                        "_": ""
                    }
                ],
                "v42": [
                    {
                        "_": "1"
                    }
                ],
                "v48": [
                    {
                        "_": "",
                        "l": "pt",
                        "h": "Sumário"
                    },
                    {
                        "_": "",
                        "l": "en",
                        "h": "Table of contents"
                    },
                    {
                        "_": "",
                        "l": "es",
                        "h": "Sumario"
                    }
                ],
                "v31": [
                    {
                        "_": "31"
                    }
                ],
                "v32": [
                    {
                        "_": "8"
                    }
                ]
            },
            "publication_year": "1998",
            "code_title": [
                "1414-431X",
                "0100-879X"
            ],
            "publication_date": "1998-08"
        },
        "doaj_id": "a9179b02560840199a817080b81d5792",
        "sent_doaj": "False",
        "normalized": {
            "article": {
                "v70": {
                    "p": [
                        true
                    ]
                }
            }
        },
        "code": "S0100-879X1998000800011",
        "updated_at": "2016-06-30",
        "collection": "scl",
        "code_issue": "998-08",
        "article": {
            "v112": [
                {
                    "_": "19970224"
                }
            ],
            "v30": [
                {
                    "_": "Braz J Med Biol Res"
                }
            ],
            "v117": [
                {
                    "_": "other"
                }
            ],
            "v35": [
                {
                    "_": "0100-879X"
                }
            ],
            "v113": [
                {
                    "_": "May 21, 1998"
                }
            ],
            "v70": [
                {
                    "i": "A01",
                    "d": "Departamento de Ciências Fisiológicas, Centro de Ciências Biológicas",
                    "_": "Universidade Estadual de Londrina"
                }
            ],
            "v705": [
                {
                    "_": "S"
                }
            ],
            "v701": [
                {
                    "_": "1"
                }
            ],
            "v706": [
                {
                    "_": "h"
                }
            ],
            "v58": [
                {
                    "_": "CNPq"
                },
                {
                    "_": "CPG-UEL"
                }
            ],
            "v111": [
                {
                    "_": "February 24, 1997"
                }
            ],
            "v1": [
                {
                    "_": "bjmbr"
                }
            ],
            "v71": [
                {
                    "_": "sc"
                }
            ],
            "v882": [
                {
                    "n": "8",
                    "v": "31",
                    "_": ""
                }
            ],
            "v91": [
                {
                    "_": "19980921"
                }
            ],
            "v700": [
                {
                    "_": "2"
                }
            ],
            "v120": [
                {
                    "_": "2.0"
                }
            ],
            "v83": [
                {
                    "a": "This study evaluates the influence of different concentrations of calcium on blood pressure of normotensive rats. Four groups of Wistar rats (A, B, C and D) had free access to modified isocaloric and isoproteic diets containing 0.2, 0.5, 2 and 4 g% calcium as calcium carbonate for a period of 30 days. Systolic and diastolic arterial blood pressures were monitored in awake rats by the indirect tail cuff method using a Physiograph equipped with transducers and preamplifiers. Body weight and length and food intake were monitored. Under the conditions of the present experiment, the systolic and diastolic arterial blood pressures of group D rats fed a diet containing 4 g% calcium were significantly (P&lt;0.05) lower compared to rats of the other groups.",
                    "l": "en",
                    "_": ""
                }
            ],
            "v2": [
                {
                    "_": "S0100-879X(98)03100811"
                }
            ],
            "v42": [
                {
                    "_": "1"
                }
            ],
            "v65": [
                {
                    "_": "19980800"
                }
            ],
            "v121": [
                {
                    "_": "11"
                }
            ],
            "v72": [
                {
                    "_": "20"
                }
            ],
            "v10": [
                {
                    "1": "A01",
                    "n": "N.",
                    "_": "",
                    "s": "Buassi",
                    "r": "ND"
                }
            ],
            "v702": [
                {
                    "_": "C:\\SciELO\\Serial\\BJMBR\\v31n8\\Markup\\2845c.htm"
                }
            ],
            "v114": [
                {
                    "_": "19980521"
                }
            ],
            "v12": [
                {
                    "l": "en",
                    "_": "High dietary calcium decreases blood pressure in normotensive rats"
                }
            ],
            "v992": [
                {
                    "_": "scl"
                }
            ],
            "v49": [
                {
                    "_": "BJMBR080"
                }
            ],
            "v880": [
                {
                    "_": "S0100-879X1998000800011"
                }
            ],
            "v936": [
                {
                    "y": "1998",
                    "i": "0100-879X",
                    "o": "8",
                    "_": ""
                }
            ],
            "v978": [
                {
                    "d": "nd",
                    "_": ""
                },
                {
                    "l": "en",
                    "k": "calcium carbonate",
                    "t": "m",
                    "_": ""
                },
                {
                    "l": "en",
                    "k": "arterial blood pressure",
                    "t": "m",
                    "_": ""
                },
                {
                    "l": "en",
                    "k": "dietary calcium",
                    "t": "m",
                    "_": ""
                }
            ],
            "v40": [
                {
                    "_": "en"
                }
            ],
            "v14": [
                {
                    "f": "1099",
                    "_": ""
                },
                {
                    "l": "1101",
                    "_": ""
                }
            ],
            "v977": [
                {
                    "l": "en",
                    "_": "High dietary calcium decreases blood pressure in normotensive rats"
                }
            ],
            "v38": [
                {
                    "_": "TAB"
                }
            ],
            "v31": [
                {
                    "_": "31"
                }
            ],
            "v4": [
                {
                    "_": "v31n8"
                }
            ],
            "v85": [
                {
                    "d": "nd",
                    "_": ""
                },
                {
                    "l": "en",
                    "k": "calcium carbonate",
                    "t": "m",
                    "_": ""
                },
                {
                    "l": "en",
                    "k": "arterial blood pressure",
                    "t": "m",
                    "_": ""
                },
                {
                    "l": "en",
                    "k": "dietary calcium",
                    "t": "m",
                    "_": ""
                }
            ],
            "v32": [
                {
                    "_": "8"
                }
            ]
        },
        "processing_date": "1998-09-21",
        "code_title": [
            "1414-431X",
            "0100-879X"
        ],
        "publication_date": "1998-08"

    }

Formato XML DOAJ
================

``GET /api/v1/article/?code=S0100-879X1998000800011&format=xmldoaj``

Resposta:

.. code-block:: xml

    ...
    <contrib-group>
        <contrib contrib-type="author">
            <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
            <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
            <name>
                <surname>Einstein</surname>
                <given-names>Albert</given-names>
            </name>
            ...
        </contrib>
        <contrib contrib-type="author">
            <contrib-id contrib-id-type="lattes">4760273612238540</contrib-id>
            <name>
                <surname>Meneghini</surname>
                <given-names>Rogerio</given-names>
            </name>
            ...
        </contrib>
        ...
    </contrib-group>
    ...

.. code-block:: xml

    <records>
        <record>
            <publisher>Associação Brasileira de Divulgação Científica</publisher>
            <journalTitle>Brazilian Journal of Medical and Biological Research</journalTitle>
            <issn>1414-431X</issn>
            <publicationDate>1998-08-00</publicationDate>
            <volume>31</volume>
            <issue>8</issue>
            <startPage>1099</startPage>
            <endPage>1101</endPage>
            <doi>10.1590/S0100-879X1998000800011</doi>
            <publisherRecordId>S0100-879X1998000800011</publisherRecordId>
            <documentType>rapid-communication</documentType>
            <title language="eng">High dietary calcium decreases blood pressure in normotensive rats</title>
            <authors>
                <author>
                    <name>N. Buassi</name>
                    <affiliationId>A01</affiliationId>
                </author>
            </authors>
            <affiliationsList>
                <affiliationName affiliationId="A01">Universidade Estadual de Londrina</affiliationName>
            </affiliationsList>
            <abstract language="eng">This study evaluates the influence of different concentrations of calcium on blood pressure of normotensive rats. Four groups of Wistar rats (A, B, C and D) had free access to modified isocaloric and isoproteic diets containing 0.2, 0.5, 2 and 4 g% calcium as calcium carbonate for a period of 30 days. Systolic and diastolic arterial blood pressures were monitored in awake rats by the indirect tail cuff method using a Physiograph equipped with transducers and preamplifiers. Body weight and length and food intake were monitored. Under the conditions of the present experiment, the systolic and diastolic arterial blood pressures of group D rats fed a diet containing 4 g% calcium were significantly (P<0.05) lower compared to rats of the other groups.</abstract>
            <fullTextUrl format="html">http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0100-879X1998000800011&lng=en&tlng=en</fullTextUrl>
            <keywords language="eng">
                <keyword>calcium carbonate</keyword>
                <keyword>arterial blood pressure</keyword>
                <keyword>dietary calcium</keyword>
            </keywords>
        </record>
    </records>
