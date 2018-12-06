# Sobre a gestão das informações sobre coleções

A partir de 30/08/2018 a gestão das informações sobre as coleções passou a ser
realizada por meio de manipulação direta ao arquivo ``collections.json``, 
presente neste diretório. O arquivo conta com um *array* de objetos com os
seguintes atributos:

```javascript
{
  "acron": "scl",
  "code": "scl",
  "domain": "www.scielo.br",
  "acron2": "br",
  "name": {
    "en": "Brazil",
    "pt": "Brasil",
    "es": "Brasil"
  },
  "has_analytics": true,
  "original_name": "Brasil",
  "status": "certified",
  "type": "journals",
  "is_active": true
},
```

Atributo      | Descrição
--------      | ---------
acron         | acrônimo da coleção
code          | identificador da coleção no ArticleMeta
domain        | website da coleção
acron2        | acrônimo alternativo da coleção
name          | dicionário contendo o nome da coleção nos 3 idiomas oficiais da Rede
has_analytics | se suas métricas estão disponíveis em analytics.scielo.org
original_name | o nome da coleção no seu idioma original
status        | indica se trata-se de uma coleção certificada (certified), de divulgação científica (diffusion), em desenvolvimento (development) ou Scielito (independent)
type          | indica se trata-se de uma coleção de periódicos ou de livros
is_active     | valor booleano que indica se a coleção está ativa ou foi descontinuada

