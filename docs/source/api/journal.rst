=========
/journal/
=========

Retorna os metadados de um periódico.

Parâmetros:

    +------------+-----------------------------------------------------+-------------+
    | Paremetros | Descrição                                           | Obrigatório |
    +============+=====================================================+=============+
    | **issn**   | ISSN do periódico no SciELO                         | sim         |
    +------------+-----------------------------------------------------+-------------+
    | collection | Acrônimo de três letras de coleções SciELO          | não         |
    +------------+-----------------------------------------------------+-------------+
    | callback   | JSONP callback method                               | não         |
    +------------+-----------------------------------------------------+-------------+


Parâmetros obrigatórios:

    *issn* ISSN do periódico no SciELO, ex: 2359-0769

--------
Exemplos
--------

``GET /api/v1/journal/?issn=2359-0769``

Resposta:

.. code-block:: json

    [

        {
            "v930": [
                {
                    "_": "rs"
                }
            ],
            "v51": [
                {
                    "_": "",
                    "a": "20160000",
                    "b": "C"
                }
            ],
            "v541": [
                {
                    "_": "BY-NC"
                }
            ],
            "v66": [
                {
                    "_": "art"
                }
            ],
            "v480": [
                {
                    "_": "Universidade de Fortaleza, Programa de Pós-Graduação em Psicologia"
                }
            ],
            "v901": [
                {
                    "_": "Esta publicación tiene como misión difundir las construcciones científicas más significativas llevadas a cabo en torno a los temas: Sujeto y sufrimiento psíquico, Sociedad, Cultura y Organizaciones Sociales, presentados en forma de artículos originales, informes de investigación, estudios teóricos, revisiones sistemáticas de la literatura, reseñas de libros o películas y entrevistas.",
                    "l": "es"
                },
                {
                    "_": "A Revista Subjetividades é uma continuidade da Revista Mal-estar e Subjetividade, é uma publicação do Programa de Pós Graduação em Psicologia da UNIFOR e tem como missão divulgar as mais significativas construções acadêmicas, científicas e artísticas realizadas em torno dos temas: Sujeito, Sofrimento psíquico, Sociedade, Cultura e Organizações Sociais, apresentadas na forma de artigos originais, comunicações, relatos de pesquisas, estudos teóricos, revisões sistemáticas de literatura, resenhas de livros ou filmes e entrevistas. Seu corpo editorial é composto por representantes de diversas áreas da psicologia que refletem os interesses de pesquisa do nosso programa e suas relações com diferentes ambientes acadêmicos e institucionais.",
                    "l": "pt"
                },
                {
                    "_": "Revista Subjetividades (Journal Subjectivities) is a peer-reviewed, online, and free access journal published three times a year by the Psychology Post-Graduation programme, Universidade de Fortaleza (Ceará, Brazil). The journal brings together scholarship from different areas of psychology and related fields in Human, Social and Health Sciences.",
                    "l": "en"
                }
            ],
            "update_date": "2016-11-04",
            "v992": [
                {
                    "_": "psi"
                }
            ],
            "code": "2359-0769",
            "v935": [
                {
                    "_": "2359-0777"
                }
            ],
            "v310": [
                {
                    "_": "BR"
                }
            ],
            "v943": [
                {
                    "_": "20161209"
                }
            ],
            "v854": [
                {
                    "_": "PSYCHOLOGY"
                },
                {
                    "_": "PSYCHOLOGY, APPLIED"
                }
            ],
            "v350": [
                {
                    "_": "es"
                },
                {
                    "_": "en"
                },
                {
                    "_": "pt"
                }
            ],
            "v940": [
                {
                    "_": "20160919"
                }
            ],
            "v400": [
                {
                    "_": "2359-0769"
                }
            ],
            "v117": [
                {
                    "_": "other"
                }
            ],
            "v951": [
                {
                    "_": "Sandra"
                }
            ],
            "v50": [
                {
                    "_": "C"
                }
            ],
            "v441": [
                {
                    "_": "Applied Social Sciences"
                }
            ],
            "v302": [
                {
                    "_": "14"
                }
            ],
            "processing_date": "2016-12-01",
            "v150": [
                {
                    "_": "Rev. Subj."
                }
            ],
            "v301": [
                {
                    "_": "2014"
                }
            ],
            "v230": [
                {
                    "_": "Journal of Subjectivities"
                }
            ],
            "v435": [
                {
                    "_": "2359-0769",
                    "t": "PRINT"
                },
                {
                    "_": "2359-0777",
                    "t": "ONLIN"
                }
            ],
            "v303": [
                {
                    "_": "1"
                }
            ],
            "v340": [
                {
                    "_": "B"
                }
            ],
            "v10": [
                {
                    "_": "UNIFOR"
                }
            ],
            "v5": [
                {
                    "_": "S"
                }
            ],
            "v67": [
                {
                    "_": "sub"
                }
            ],
            "v320": [
                {
                    "_": "CE"
                }
            ],
            "creted_at": "2016-09-19",
            "updated_date": "2016-11-04",
            "v63": [
                {
                    "_": "Av. Washington Soares, 1321 - Bloco N Sala 13"
                },
                {
                    "_": "Bairro Edson Queiroz"
                },
                {
                    "_": "CEP: 60811-905 - Fortaleza - CE"
                },
                {
                    "_": "Tel: (85) 3477.3446"
                },
                {
                    "_": "Fax: (85) 3477.3063"
                }
            ],
            "v900": [
                {
                    "_": "*A Revista Subjetividades (ISSN 2359-0777) é uma continuação da Revista Mal-Estar e Subjetividade (ISSN 2175-3644), avaliada pela CAPES como B1."
                }
            ],
            "collection": "psi",
            "v35": [
                {
                    "_": "ONLIN"
                }
            ],
            "v610": [
                {
                    "_": "Revista Mal-Estar e Subjetividade"
                }
            ],
            "issns": [
                "2359-0777",
                "2359-0769"
            ],
            "v360": [
                {
                    "_": "es"
                },
                {
                    "_": "fr"
                },
                {
                    "_": "en"
                },
                {
                    "_": "pt"
                }
            ],
            "v440": [
                {
                    "_": "PSICOLOGIA"
                },
                {
                    "_": "PSICOLOGIA APLICADA"
                }
            ],
            "v942": [
                {
                    "_": "20160919"
                }
            ],
            "v950": [
                {
                    "_": "Sandra"
                }
            ],
            "v151": [
                {
                    "_": "Rev. Subj."
                }
            ],
            "v64": [
                {
                    "_": "revistasubjetividades@gmail.com"
                }
            ],
            "updated_at": "2017-03-28",
            "v540": [
                {
                    "_": "",
                    "l": "es",
                    "t": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by-nc/3.0/deed.es\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"http://i.creativecommons.org/l/by-nc/3.0/88x31.png\" /></a> Todo el contenido de esta revista, excepto dónde está identificado, est&#225; bajo una <a rel=\"license\" href=\"http://creativecommons.org/licenses/by-nc/3.0/deed.es\">Licencia Creative Commons</a>"
                },
                {
                    "_": "",
                    "l": "pt",
                    "t": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by-nc/3.0/deed.pt\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"http://i.creativecommons.org/l/by-nc/3.0/80x15.png\" /></a> Todo o conteúdo deste periódico, exceto onde est&#225 identificado, est&#225; licenciado sob uma <a rel=\"license\" href=\"http://creativecommons.org/licenses/by-nc/3.0/deed.pt\">Licen&#231;a Creative Commons</a>"
                },
                {
                    "_": "",
                    "l": "en",
                    "t": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by-nc/3.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"http://i.creativecommons.org/l/by-nc/3.0/80x15.png\" /></a> All the contents of this journal, except where otherwise noted, is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by-nc/3.0/\">Creative Commons Attribution License</a>"
                }
            ],
            "v490": [
                {
                    "_": "Fortaleza"
                }
            ],
            "v880": [
                {
                    "_": "2359-0769"
                }
            ],
            "v6": [
                {
                    "_": "c"
                }
            ],
            "v692": [
                {
                    "_": "http://ojs.unifor.br/index.php/rmes/login"
                }
            ],
            "v330": [
                {
                    "_": "CT"
                }
            ],
            "v380": [
                {
                    "_": "T"
                }
            ],
            "v68": [
                {
                    "_": "rs"
                }
            ],
            "v62": [
                {
                    "_": "Universidade de Fortaleza - Revista Subjetividades"
                }
            ],
            "v691": [
                {
                    "_": "100000000000000000000000"
                }
            ],
            "v941": [
                {
                    "_": "20161201"
                }
            ],
            "v100": [
                {
                    "_": "Revista Subjetividades"
                }
            ],
            "v85": [
                {
                    "_": "nd"
                }
            ]
        }

    ]