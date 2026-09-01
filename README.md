# Articles Meta


[![Build Status](https://travis-ci.org/scieloorg/articles_meta.svg)](https://travis-ci.org/scieloorg/articles_meta)
[![a](https://images.microbadger.com/badges/image/scieloorg/articles_meta.svg)](https://hub.docker.com/r/scieloorg/articles_meta)
[![b](https://images.microbadger.com/badges/version/scieloorg/articles_meta.svg)](https://hub.docker.com/r/scieloorg/articles_meta)


Webservices para fornecer metadados de artigos SciELO da Rede SciELO (armazenados no MongoDB).

## Como utilizar esta imagem

```shell
    $ docker run --name my-articlemeta -d my-articlemeta
```


### Como configurar o MONGODB_HOST

```shell
    $ docker run --name my-articlemeta -e MONGODB_HOST=my_eshost:27017 -d my-articlemeta my-articlemeta
```

Os serviços ativos nesta imagem são:

 * Web API: 127.0.0.1:8000
 * Thrift Server: 127.0.0.1:11620


É possível mapear essas portas para o hosting dos containers da seguinte forma:

```shell
    $ docker run --name my-articlemeta -e MONGODB_HOST=my_eshost:27017 -p 8000:8000 -p 11620:11620 -d my-articlemeta my-articlemeta
```

# Como executar comandos de processamentos

Para executar os processamentos disponíveis em console scripts, executar:

Carga de Licenças de uso:

```shell
   $ docker exec -i -t my-articlemeta articlemeta_loadlicenses --help
```

# Fixtures

Procedimento para popular a instância de desenvolvimento a partir de fixtures disponibilizadas pelo SciELO.

1. Para execução dos procedimentos que adicionam dados no banco é necessário que o ambiente de desenvolvimento do article_meta esteja rodando a aplicação
2. Baixar a fixture de desenvolvimento versão light com 4 periódicos, execute: ``wget https://minio.scielo.br/dev/fixtures/article_meta.zip`` 
3. Extraia o conteúdo, execute: ``unzip article_meta.zip``
4. Repare que uma pasta chamada article_meta foi criada e dentro dela há arquivos .bson, .json.
5. Acesse a pasta **article_meta**, execute: ``cd article_meta``
6. Utilizando **mongorestore** realize a recuperação do banco de dados apontando para o endereço que está rodando o seu mongo local, exemplo: ``mongorestore --host=localhost --port=27017 --db=articlemeta --dir .``


# Nota

Para histórico de desenvolvimento anterior ao registrado neste repositório, verificar: https://bitbucket.org/scieloorg/xmlwos

https://developer.atlassian.com/cloud/acli/guides/introduction/#atlassian-command-line-interface--cli-

Markdown: Sintaxis
================

<ul id="ProjectSubmenu">
    <li><a href="/projects/markdown/" title="Página principal del proyecto Markdown">Principal</a></li>
    <li><a href="/projects/markdown/basics" title="Conceptos básicos de Markdown">Conceptos básicos</a></li>
    <li><a class="selected" title="Documentación de sintaxis de Markdown">Sintaxis</a></li>
    <li><a href="/projects/markdown/license" title="Información sobre precios y licencias">Licencia</a></li>
    <li><a href="/projects/markdown/dingus" title="Formulario web Markdown en línea">Dingus</a></li>
</ul>


* [Descripción general](#descripción general)
    * [Filosofía](#filosofía)
    * [HTML en línea](#html)
    * [Escape automático para caracteres especiales](#autoescape)
* [Elementos de bloque](#block)
    * [Párrafos y saltos de línea](#p)
    * [Encabezados](#encabezado)
    * [Citas en bloque](#blockquote)
    * [Listas](#list)
    * [Bloques de código](#precode)
    * [Reglas horizontales](#hr)
* [Elementos Span](#span)
    * [Enlaces](#link)
    * [Énfasis](#em)
    * [Código](#código)
    * [Imágenes](#img)
* [Varios](#misc)
    * [Escapes de barra invertida](#barra invertida)
    * [Enlaces automáticos](#autolink)


**Nota:** Este documento está escrito en Markdown;
Puedes [ver la fuente agregando '.text' a la URL][src].

  [src]: /projects/markdown/syntax.text

* * *

<h2 id="overview">Descripción general</h2>

<h3 id="philosophy">Filosofía</h3>

Markdown está diseñado para ser lo más fácil de leer y de escribir posible.

Sin embargo, se hace hincapié en la legibilidad por encima de todo. Un documento con formato Markdown
El documento debe poder publicarse tal cual, como texto plano, sin necesidad de buscar
como si hubiera sido marcado con etiquetas o instrucciones de formato.
La sintaxis de Markdown ha sido influenciada por varios sistemas de conversión de texto a HTML existentes.
filtros -- incluyendo [Setext][1], [atx][2], [Textile][3], [reStructuredText][4],
[Grutatext][5] y [EtText][6] -- la única fuente más grande de
La sintaxis de Markdown se inspira en el formato de correo electrónico de texto plano.

  [1]: http://docutils.sourceforge.net/mirror/setext.html
  [2]: http://www.aaronsw.com/2002/atx/
  [3]: https://web.archive.org/web/20021226035527/http://textism.com/tools/textile/
  [4]: http://docutils.sourceforge.net/rst.html
  [5]: http://www.triptico.com/software/grutatxt.html
  [6]: http://ettext.taint.org/doc/

Para ello, la sintaxis de Markdown se compone enteramente de signos de puntuación.
caracteres, que los signos de puntuación han sido cuidadosamente elegidos así
para que parezca lo que quieren decir. Por ejemplo, asteriscos alrededor de una palabra.
parecen *énfasis*. Las listas de Markdown parecen, bueno, listas. Incluso
Las citas en bloque se ven como pasajes de texto citados, suponiendo que alguna vez...
correo electrónico utilizado.



<h3 id="html">HTML incorporado</h3>

La sintaxis de Markdown está destinada a un solo propósito: ser utilizada como
formato para *escribir* para la web.

Markdown no es un reemplazo para HTML, ni siquiera se le acerca.
La sintaxis es muy pequeña, correspondiendo solo a un subconjunto muy pequeño de
Etiquetas HTML. La idea *no* es crear una sintaxis que lo haga más fácil
para insertar etiquetas HTML. En mi opinión, las etiquetas HTML ya son fáciles de usar.
insertar. La idea de Markdown es hacer que sea fácil de leer, escribir y
editar prosa. HTML es un formato de *publicación*; Markdown es un formato de *escritura*.
formato. Por lo tanto, la sintaxis de formato de Markdown solo aborda problemas que
puede transmitirse en texto plano.

Para cualquier marcado que no esté cubierto por la sintaxis de Markdown, simplemente
usar HTML en sí mismo. No hay necesidad de anteponerle ni de delimitarlo.
indica que estás cambiando de Markdown a HTML; simplemente usa
las etiquetas.

Las únicas restricciones son que los elementos HTML de nivel de bloque, por ejemplo `<div>`,
`<table>`, `<pre>`, `<p>`, etc. -- deben estar separados del texto circundante.
contenido por líneas en blanco, y las etiquetas de inicio y fin del bloque deberían
no se sangra con tabulaciones o espacios. Markdown es lo suficientemente inteligente como para no
para agregar etiquetas `<p>` adicionales (no deseadas) alrededor de las etiquetas de nivel de bloque HTML.

Por ejemplo, para agregar una tabla HTML a un artículo de Markdown:

    Este es un párrafo normal.

    <tabla>
        <tr>
            <td>Comida</td>
        </tr>
    </tabla>

    Este es otro párrafo normal.

Tenga en cuenta que la sintaxis de formato Markdown no se procesa dentro del nivel de bloque.
Etiquetas HTML. Por ejemplo, no puedes usar el estilo Markdown `*énfasis*` dentro de una
Bloque HTML.

Las etiquetas HTML de nivel span, por ejemplo `<span>`, `<cite>` o `<del>`, pueden ser
Se puede usar en cualquier parte de un párrafo, elemento de lista o encabezado de Markdown. Si
Si lo desea, incluso puede usar etiquetas HTML en lugar del formato Markdown; por ejemplo, si
Preferirías usar etiquetas HTML `<a>` o `<img>` en lugar de Markdown.
Sintaxis de enlace o imagen, adelante.

A diferencia de las etiquetas HTML de nivel de bloque, la sintaxis Markdown *se* procesa dentro de
etiquetas de nivel de span.


<h3 id="autoescape">Escape automático de caracteres especiales</h3>

En HTML, hay dos caracteres que requieren un tratamiento especial: `<`
y `&`. Los corchetes angulares izquierdos se utilizan para iniciar etiquetas; los ampersands son
Se utiliza para denotar entidades HTML. Si desea utilizarlas como literales.
caracteres, debe escaparlos como entidades, por ejemplo `<`, y
`&`.

Los signos de ampersand en particular son un quebradero de cabeza para los escritores web. Si quieres
Para escribir sobre 'AT&T', necesitas escribir '`AT&T`'. Incluso necesitas
Escapar de los signos de ampersand dentro de las URL. Por lo tanto, si quieres enlazar a:

    http://images.google.com/images?num=30&q=larry+bird

Debes codificar la URL de la siguiente manera:

    http://images.google.com/images?num=30&q=larry+bird

en el atributo `href` de tu etiqueta de anclaje. No hace falta decir que esto es fácil de hacer.
Olvídalo, y probablemente sea la fuente más común de validación HTML.
errores en sitios web que, por lo demás, están bien etiquetados.

Markdown te permite usar estos caracteres de forma natural, encargándose de
todo el escape necesario para usted. Si utiliza un ampersand como parte de
una entidad HTML, permanece sin cambios; de lo contrario, se traducirá.
en `&`.

Por lo tanto, si desea incluir un símbolo de derechos de autor en su artículo, puede escribir:

    &Copiar;

y Markdown lo dejará en paz. Pero si escribes:

    AT&T

Markdown lo traducirá a:

    AT&T

De manera similar, debido a que Markdown admite [HTML en línea](#html), si usa
Corchetes angulares como delimitadores para etiquetas HTML, Markdown los tratará como
tal. Pero si escribes:

    4 < 5

Markdown lo traducirá a:

    4 < 5

Sin embargo, dentro de los bloques y segmentos de código Markdown, los corchetes angulares y
Los signos de ampersand se codifican *siempre* automáticamente. Esto facilita su uso.
Markdown para escribir sobre código HTML. (A diferencia del HTML sin formato, que es un
formato terrible para escribir sobre la sintaxis HTML, porque cada `<`
y el símbolo `&` en tu código de ejemplo debe escaparse.)


* * *


<h2 id="block">Elementos de bloque</h2>


<h3 id="p">Párrafos y saltos de línea</h3>

Un párrafo es simplemente una o más líneas de texto consecutivas, separadas
por una o más líneas en blanco. (Una línea en blanco es cualquier línea que parezca una
línea en blanco: una línea que no contiene nada más que espacios o tabulaciones se considera
(en blanco.) Los párrafos normales no deben sangrarse con espacios ni tabulaciones.

La implicación de la regla de "una o más líneas de texto consecutivas" es
que Markdown admite párrafos de texto con "ajuste de línea forzado". Esto difiere
significativamente diferente de la mayoría de los demás formateadores de texto a HTML (incluido Movable
La opción "Convertir saltos de línea" de Type traduce cada salto de línea.
carácter en un párrafo dentro de una etiqueta `<br />`.

Cuando *sí* quieres insertar una etiqueta de salto de línea `<br />` usando Markdown,
Finaliza la línea con dos o más espacios y, a continuación, pulsa Intro.

Sí, esto requiere un poco más de esfuerzo para crear un `<br />`, pero un simple
La regla "cada salto de línea es un `<br />`" no funcionaría para Markdown.
El estilo de correo electrónico de Markdown [blockquoting][bq] y los elementos de lista de varios párrafos [list items][l]
Funcionan mejor, y tienen mejor aspecto, cuando se les da formato con saltos de línea pronunciados.

  [bq]: #blockquote
  [l]: #lista



<h3 id="header">Encabezados</h3>

Markdown admite dos estilos de encabezados, [Setext] [1] y [atx] [2].

Los encabezados de estilo Setext se "subrayan" usando signos de igual (para el primer nivel).
encabezados) y guiones (para encabezados de segundo nivel). Por ejemplo:

    Este es un H1
    =============

    Este es un H2
    -------------

Cualquier cantidad de signos `=` o `-` subrayados funcionará.

Los encabezados estilo ATX utilizan de 1 a 6 caracteres de almohadilla al comienzo de la línea,
correspondientes a los niveles de encabezado 1-6. Por ejemplo:

    # Este es un H1

    ## Este es un H2

    ###### Este es un H6

Opcionalmente, puede "cerrar" los encabezados de estilo atx. Esto es puramente
cosmético: puedes usarlo si crees que se ve mejor. El
Los hashes de cierre ni siquiera necesitan coincidir con el número de hashes.
utilizado para abrir el encabezado. (El número de hashes de apertura)
determina el nivel de encabezado.) :

    # Esto es un H1 #

    ## Esto es un H2 ##

    ### Esto es un H3 ######


<h3 id="blockquote">Citas en bloque</h3>

Markdown utiliza caracteres `>` al estilo del correo electrónico para las citas en bloque. Si estás
Si está familiarizado con citar fragmentos de texto en un mensaje de correo electrónico, entonces...
saber cómo crear una cita en bloque en Markdown. Se ve mejor si lo haces
Envuelve el texto y coloca un `>` antes de cada línea:

    > Esta es una cita en bloque con dos párrafos. Lorem ipsum dolor siéntate amet,
    > consectetuer élite adipiscente. Aliquam hendrerit mi posuere lectus.
    > Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
    >
    > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. suspendido
    > id sem consectetuer libero luctus adipiscing.

Markdown te permite ser perezoso y solo poner el `>` antes del primer
línea de un párrafo envuelto en negrita:

    > Esta es una cita en bloque con dos párrafos. Lorem ipsum dolor siéntate amet,
    consectetuer élite adipiscente. Aliquam hendrerit mi posuere lectus.
    Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.

    > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. suspendido
    id sem consectetuer libero luctus adipiscing.

Las citas en bloque pueden anidarse (es decir, una cita en bloque dentro de otra) mediante
agregando niveles adicionales de `>`:

    > Este es el primer nivel de cotización.
    >
    >> Esto es una cita anidada.
    >
    > Volver al primer nivel.

Las citas en bloque pueden contener otros elementos de Markdown, incluidos encabezados, listas,
y bloques de código:

	> ## Este es un encabezado.
	>
	> 1. Este es el primer elemento de la lista.
	> 2. Este es el segundo elemento de la lista.
	>
	Aquí tienes un ejemplo de código:
	>
	> return shell_exec("echo $input | $markdown_script");

Cualquier editor de texto decente debería facilitar la citación al estilo de los correos electrónicos.
Por ejemplo, con BBEdit, puedes hacer una selección y elegir Incrementar.
Nivel de cita desde el menú Texto.


<h3 id="list">Listas</h3>

Markdown admite listas ordenadas (numeradas) y no ordenadas (con viñetas).

Las listas no ordenadas utilizan asteriscos, signos más y guiones, indistintamente.
-- como marcadores de lista:

    * Rojo
    * Verde
    * Azul

es equivalente a:

    + Rojo
    + Verde
    + Azul

y:

    - Rojo
    - Verde
    - Azul

Las listas ordenadas utilizan números seguidos de puntos:

    1. Ave
    2. McHale
    3. Parroquia

Es importante tener en cuenta que los números reales que utilice para marcar el
La lista no tiene ningún efecto en la salida HTML que produce Markdown. El HTML
El Markdown que se genera a partir de la lista anterior es:

    <ol>
    <li>Pájaro</li>
    <li>McHale</li>
    <li>Parroquia</li>
    </ol>

Si en cambio escribieras la lista en Markdown de esta manera:

    1. Ave
    1. McHale
    1. Parroquia

o incluso:

    3. Pájaro
    1. McHale
    8. Parroquia

obtendrías exactamente la misma salida HTML. La cuestión es que, si quieres,
Puedes usar números ordinales en tus listas Markdown ordenadas, de modo que
Los números en tu código fuente coinciden con los números en tu HTML publicado.
Pero si quieres ser perezoso, no tienes por qué serlo.

Sin embargo, si utiliza la numeración de listas perezosa, aún debe comenzar con la
lista con el número 1. En algún momento futuro, Markdown podría admitir
comenzar las listas ordenadas en un número arbitrario.

Los marcadores de lista normalmente comienzan en el margen izquierdo, pero pueden estar indentados por
hasta tres espacios. Los marcadores de lista deben ir seguidos de uno o más espacios.
o una pestaña.

Para que las listas tengan un aspecto más estético, puedes usar sangrías francesas para envolver los elementos:

    * Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
        Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
        viverra nec, fringilla in, laoreet vitae, risus.
    * Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
        Suspendisse id sem consectetuer libero luctus adipiscing.

Pero si quieres ser perezoso, no tienes por qué hacerlo:

    * Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
    viverra nec, fringilla in, laoreet vitae, risus.
    * Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
    Suspendisse id sem consectetuer libero luctus adipiscing.

Si los elementos de la lista están separados por líneas en blanco, Markdown ajustará el
elementos entre etiquetas `<p>` en la salida HTML. Por ejemplo, esta entrada:

    * Pájaro
    * Magia

se convertirá en:

    <ul>
    <li>Pájaro</li>
    <li>Magia</li>
    </ul>

Pero esto:

    * Pájaro

    * Magia

se convertirá en:

    <ul>
    <li><p>Pájaro</p></li>
    <li><p>Magia</p></li>
    </ul>

Los elementos de la lista pueden constar de varios párrafos. Cada párrafo subsiguiente
El párrafo en un elemento de lista debe tener una sangría de 4 espacios.
o una pestaña:

    1. Este es un elemento de lista con dos párrafos. Lorem ipsum dolor
        sit amet, consectetuer adipiscing elit. Aliquam Hendrerit
        mi posuere lectus.

        Vestibulum enim wisi, viverra nec, fringilla in, laoreet
        vitae, risus. Donec sit amet nisl. Aliquam sempre ipsum
        sit amet velit.

    2. Suspendisse id sem consectetuer libero luctus adipiscing.

Queda bien si indentas cada línea de la siguiente
párrafos, pero aquí de nuevo, Markdown te permitirá ser
perezoso:

    * Este es un elemento de lista con dos párrafos.

        Este es el segundo párrafo del elemento de la lista.
    Sólo es necesario sangrar la primera línea. Lorem ipsum dolor
    sit amet, consectetuer adipiscing elit.

    * Otro elemento de la misma lista.

Para insertar una cita en bloque dentro de un elemento de lista, utilice el símbolo `>` de la cita en bloque.
Los delimitadores deben ir indentados:

    * Un elemento de lista con una cita en bloque:

        > Esto es una cita en bloque
        > dentro de un elemento de la lista.

Para colocar un bloque de código dentro de un elemento de lista, el bloque de código necesita
Debe tener sangría *dos veces*: 8 espacios o dos tabulaciones:

    * Un elemento de lista con un bloque de código:

            <Aquí va el código>


Vale la pena señalar que es posible activar una lista ordenada mediante
accidente, escribiendo algo como esto:

    1986. ¡Qué gran temporada!

En otras palabras, una secuencia *número-período-espacio* al comienzo de un
línea. Para evitar esto, puede escapar el punto con una barra invertida:

    1986. ¡Qué gran temporada!



<h3 id="precode">Bloques de código</h3>

Los bloques de código preformateados se utilizan para escribir sobre programación o
código fuente de marcado. En lugar de formar párrafos normales, las líneas
Los elementos de un bloque de código se interpretan literalmente. Markdown envuelve un bloque de código.
tanto en las etiquetas `<pre>` como en las etiquetas `<code>`.

Para producir un bloque de código en Markdown, simplemente indenta cada línea del
Bloquear por al menos 4 espacios o 1 tabulación. Por ejemplo, dada esta entrada:

    Este es un párrafo normal:

        Este es un bloque de código.

Markdown generará:

    <p>Este es un párrafo normal:</p>

    <pre><code>Este es un bloque de código.
    </code></pre>

Se elimina un nivel de sangría (4 espacios o 1 tabulación) de cada
línea del bloque de código. Por ejemplo, esto:

    Aquí tienes un ejemplo de AppleScript:

        Dile a la aplicación "Foo"
            bip
        fin de decir

se convertirá en:

    <p>Aquí tienes un ejemplo de AppleScript:</p>

    <pre><code>Dile a la aplicación "Foo"
        bip
    fin de decir
    </code></pre>

Un bloque de código continúa hasta que llega a una línea que no está indentada.
(o el final del artículo).

Dentro de un bloque de código, se utilizan los signos de ampersand (`&`) y los corchetes angulares (`<` y `>`).
se convierten automáticamente en entidades HTML. Esto lo hace muy
Es fácil incluir código fuente HTML de ejemplo usando Markdown; solo hay que pegarlo.
y sangrarlo, y Markdown se encargará de la molestia de codificarlo.
Signos de ampersand y corchetes angulares. Por ejemplo, esto:

        <div class="footer">
            © 2004 Foo Corporation
        </div>

se convertirá en:

    <pre><code><div class="footer">
        © 2004 Foo Corporation
    </div>
    </code></pre>

La sintaxis Markdown estándar no se procesa dentro de los bloques de código. Por ejemplo,
Los asteriscos son simplemente asteriscos literales dentro de un bloque de código. Esto significa
También es fácil usar Markdown para escribir sobre la propia sintaxis de Markdown.



<h3 id="hr">Reglas horizontales</h3>

Puedes producir una etiqueta de línea horizontal (`<hr />`) colocando tres o
más guiones, asteriscos o guiones bajos en una línea aparte. Si usted
Si lo desea, puede usar espacios entre los guiones o asteriscos. Cada uno de los
Las siguientes líneas producirán una línea horizontal:

    * * *

    ***

    *****

    ---

    ---------------------------------------


* * *

<h2 id="span">Elementos span</h2>

<h3 id="link">Enlaces</h3>

Markdown admite dos estilos de enlaces: *en línea* y *de referencia*.

En ambos estilos, el texto del enlace está delimitado por [corchetes].

Para crear un enlace en línea, utilice inmediatamente un conjunto de paréntesis regulares.
después del corchete de cierre del texto del enlace. Dentro de los paréntesis,
Coloca la URL a donde quieres que apunte el enlace, junto con un *opcional*
Título del enlace, entre comillas. Por ejemplo:

    Este es [un ejemplo](http://example.com/ "Título") enlace en línea.

    [Este enlace](http://example.net/) no tiene atributo de título.

Producirá:

    <p>Este es <a href="http://example.com/" title="Título">
    un ejemplo de enlace en línea.

    <p><a href="http://example.net/">Este enlace</a> no tiene
    atributo título.</p>

Si te refieres a un recurso local en el mismo servidor, puedes
usar rutas relativas:

    Consulta mi página [Acerca de](/about/) para obtener más detalles.   

Los enlaces de estilo refe
