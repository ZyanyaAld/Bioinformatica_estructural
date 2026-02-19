---
title: "Estructura Cauternaria"
subtitle: "Día 04"
author: "Velazquez Aldrete Zyanya Valentina"
date: "19/02/2026"
---

## **La estructura cuaternaria es el nivel más complejo de organización proteica, formado por la asociación funcional de dos o más cadenas polipeptídicas (subunidades)** 

El texto explora la estructura cuaternaria de las proteínas, centrándose en las interfaces moleculares donde ocurren las interacciones con otras proteínas o con ácidos nucleicos (como el ADN). Estas interacciones son fundamentales para la función biológica en el contexto celular.

### 6.1 Interfaces Moleculares: Conservación y Diseño

Inspirándonos en los trabajos de Chothia y Lesk sobre la relación entre secuencia y estructura, investigaciones posteriores (como las de Aloy & Russell, 2002, y Contreras-Moreira & Collado-Vides, 2006) aplicaron el mismo análisis a las interfaces. La principal conclusión es que proteínas con secuencias similares tienden a formar interfaces similares cuando se unen a otras moléculas.

*Importancia Biológica:* Las proteínas rara vez actúan solas; su estado habitual es en complejo con otras moléculas (formando homo/heterodímeros, reconociendo ligandos, etc.). Las interfaces son, por tanto, regiones críticas para procesos como el reconocimiento de ligandos por receptores (ej. inmunoglobulinas) o la unión de factores de transcripción al ADN.

*Aplicación al Diseño de Proteínas:* Estas observaciones son la base de los algoritmos de diseño de proteínas, que a menudo se centran en modificar la interfaz para alterar la estabilidad, actividad o especificidad de una proteína.

Precaución: El texto advierte que centrarse solo en la interfaz es una simplificación. A veces, cambios en regiones alejadas del sitio de unión pueden tener un impacto crucial en la función biológica, como se ha observado en ciertos factores de transcripción (Hudson et al., 2016). El diagrama de flujo presentado muestra un protocolo genérico de diseño, pero debe considerarse como una guía general.

### 6.2 Optimización de Cadenas Laterales (Rotámeros) en Interfaces

Cuando la similitud de secuencia entre dos proteínas es alta, se puede asumir que su esqueleto peptídico no variará significativamente. Esto permite optimizar la secuencia de aminoácidos modificando las cadenas laterales.

**Método y Herramientas:**

- Rotámeros: Son las conformaciones discretas y energéticamente favorables que pueden adoptar las cadenas laterales de los aminoácidos. Se recopilan en bibliotecas (ej. a partir del PDB).

- SCWRL: Es un programa que, dada una estructura de esqueleto, predice los rotámeros óptimos para los residuos de una proteína, considerando la geometría local y las interacciones con vecinos.

### 6.3 Modelando Nucleótidos en el ADN

Al igual que SCWRL optimiza rotámeros de aminoácidos, existen herramientas y código (como el fragmento del algoritmo DNAPROT de Espinosa Angarica et al., 2008) que permiten modificar bases nitrogenadas en una doble hélice de ADN.

**Herramientas Específicas:** Para la manipulación de ácidos nucleicos, se recomienda el uso de software especializado como 3DNA, que permite desde una interfaz web o línea de comandos realizar análisis detallados y modificaciones de estructuras de ADN/ARN.

### 6.4 Interacciones no covalentes: puentes de hidrógeno en la interfaz

El estudio experimental y teórico de las interacciones entre proteínas (protein-protein interactions) ha impulsado el interés por comprender los mecanismos que explican la especificidad de su reconocimiento. Se trata de un proceso termodinámico complejo donde confluyen factores de afinidad y especificidad, aunque en numerosos casos los protagonistas principales son los puentes de hidrógeno que se establecen en la interfaz. Estos enlaces dependen directamente de la secuencia aminoacídica, dado que no todos los residuos pueden actuar como donadores o aceptores (Kortemme, Morozov, and Baker 2003).

En esta sección se aborda un nivel adicional de complejidad, pues además de muestrear resulta necesario evaluar la especificidad del reconocimiento en las interfaces modeladas, por ejemplo mediante la estimación de la formación de puentes de hidrógeno.

El punto de partida para presentar este algoritmo es la estructura del complejo de dnaA y su sitio operador, tras añadir con Open Babel los átomos de hidrógeno que pudieran faltar en el fichero en formato PDB. Partiendo del complejo disponible en el archivo PDB 1J1V, utilizado previamente en el apartado 6.3, se obtiene 1j1v_withH.pdb. Una vez realizado este paso preliminar, mediante el siguiente código es posible identificar los puentes de hidrógeno presentes en la interfaz proteína-DNA, de manera análoga a como lo haría el programa HBPLUS.

### 6.5 Interfaces entre proteína, DNA y RNA: endonucleasas CRISPR-Cas guiadas por RNA

En ocasiones no es necesario modelar una interfaz molecular desde cero, sino comprender sus características para diseñar experimentos. Este es el caso de las endonucleasas CRISPR-Cas, herramientas de edición genómica que resultan conceptualmente más sencillas de emplear que las proteínas TALEN o las endonucleasas fusionadas con dominios Zinc Finger (ZFN).

Estos sistemas se han utilizado, por ejemplo, para inducir mutaciones heredables en loci seleccionados de plantas, incluso en especies poliploides como el trigo panadero (Y. Wang et al. 2014; Lawrenson et al. 2015). Para ello es preciso realizar análisis de secuencias que permitan elegir las dianas adecuadas, normalmente secuencias únicas en el genoma. En el caso de las endonucleasas Cas (Stella, Alcon, and Montoya 2017), polipéptidos de más de 1000 aminoácidos, las secuencias diana deben seleccionarse respetando la arquitectura de la interfaz entre proteína, DNA y RNA, que requiere un motivo de entre 3 y 5 bases adyacente a la diana, denominado PAM (protospacer adjacent motif). Además de la estructura de estos complejos, resulta necesario determinar experimentalmente in vitro e in vivo la tasa de cortes no deseados y qué regiones del RNA guía (sgRNA) son más críticas para la hibridación (Cisse, Kim, and Ha 2012; T. Zheng et al. 2017). También se han empleado modelos de dinámica molecular para estudiar la mecánica de estos complejos (W. Zheng 2017).

### 6.6 Modelando interfaces moleculares por homología

Existen numerosas herramientas disponibles para modelar interfaces entre proteínas, desde opciones sencillas como InterPreTS o PPI3D, que no modifican la geometría de la estructura molde, hasta protocolos más complejos que ajustan el acoplamiento mediante docking. También hay herramientas especializadas en el estudio de interfaces en el contexto de enfermedades asociadas a mutaciones (InteractomeINSIDER) o en el diseño de anticuerpos (Lapidoth et al. 2015; Baran et al. 2017).

Se combinan algunas de las herramientas empleadas en secciones anteriores para estudiar tres factores sigma70 diferentes de la bacteria Rhizobium etli CFN42: SigA, rpoH1 y rpoH2. De ninguna de ellas se conoce actualmente su estructura en complejo con ADN, aunque se sabe que SigA reconoce con cierta especificidad el consenso CTTGACN[16-23]TATNNT, tal como se describe en detalle en el trabajo de Ramirez-Romero et al. (2006), donde además se estima la estabilidad de las regiones promotoras.

Para seleccionar estructuras molde que sirvan para construir modelos se puede, buscar directamente en el PDB. Sin embargo, en este caso resulta más eficiente consultar el repositorio 3D-footprint (Contreras-Moreira 2010), que contiene el conjunto actualizado de complejos proteína-DNA. Al introducir en el motor de búsqueda de 3D-footprint las secuencias de estas tres proteínas, se observa que el complejo 1rio_H constituye el mejor molde en todos los casos, mientras que 3iyd_F corresponde a un complejo resuelto por microscopía con baja resolución:

```bash
text
factor	logo	E-value	%IID	%Isim	%Icover	organism	complex
SigA:	cTTGACT	4e-23	100	100.0	100	THERMUS AQUATICUS	1rio_H:STRUCTURE OF BACTERIOPHAGE LAMBDA C…
>1rio_H:Sigma3_and_sigma4_domains_of_RNA_polymerase_sigma_factors;
           title=STRUCTURE OF BACTERIOPHAGE LAMBDA CI-NTD IN COMPLEX WITH SIGMA-REGION4 OF THERMUS AQUATICUS BOUND TO
           DNA organism=THERMUS AQUATICUS | interface=43,44,45,46,48,49

  Expect = 4e-23, Identities = 34/59 (57%)
  Interface: identity = 6/6 (100%) , similarity = 6.0/6 (100%) , coverage = 6/6 (100%)

Query: 614 ETTTRVLASLTPREERVLRMRFGIGMNTDHTLEEVGQQFSVTRERIRQIEAKALRKLKH 672
           E   + L+ L+ RE  VL++R G+    +HTLEEVG  F VTRERIRQIE KALRKLK+
Sbjct: 2   EELEKALSKLSEREAMVLKLRKGLIDGREHTLEEVGAYFGVTRERIRQIENKALRKLKY 60

rpoH1:	cTTGACT	3e-17	83	87.5	100	THERMUS AQUATICUS	1rio_H:STRUCTURE OF BACTERIOPHAGE LAMBDA C…
>1rio_H:Sigma3_and_sigma4...

  Expect = 3e-17, Identities = 24/56 (42%)
  Interface: identity = 5/6 (83%) , similarity = 5.2/6 (88%) , coverage = 6/6 (100%)

Query: 228 LAKAMSVLNERERRIFEARRLAED--PVTLEDLSAEFDISRERVRQIEVRAFEKVQ 281
           L KA+S L+ERE  + + R+   D    TLE++ A F ++RER+RQIE +A  K++
Sbjct: 4   LEKALSKLSEREAMVLKLRKGLIDGREHTLEEVGAYFGVTRERIRQIENKALRKLK 59

rpoH2:	cTTGACT	2e-18	67	77.5	100	THERMUS AQUATICUS	1rio_H:STRUCTURE OF BACTERIOPHAGE LAMBDA C…
>1rio_H:Sigma3_and_sigma4...

  Expect = 2e-18, Identities = 26/56 (46%)
  Interface: identity = 4/6 (67%) , similarity = 4.7/6 (78%) , coverage = 6/6 (100%)

Query: 220 LASALKHLNEREMKIISARRLAEDGA--TLEELGADLGISKERVRQIESRAMEKLR 273
           L  AL  L+ERE  ++  R+   DG   TLEE+GA  G+++ER+RQIE++A+ KL+
Sbjct: 4   LEKALSKLSEREAMVLKLRKGLIDGREHTLEEVGAYFGVTRERIRQIENKALRKLK 59
Puede observarse asimismo que el logo de 1rio_H se corresponde adecuadamente con la caja -35 descrita en el artículo de Ramirez-Romero et al. (2006):

text
cTTGACT
||||||+
CTTGACN
```

Este resultado no resulta sorprendente, dado que SigA presenta un conjunto de residuos de interfaz (aquellos que contactan con las bases nitrogenadas) conservado respecto al de 1rio_H. Sin embargo, no ocurre lo mismo con rpoH1 y rpoH2, que muestran mutaciones en dicha interfaz.

### 6.7 Modelando interfaces moleculares mediante docking

Cuando no se dispone de estructuras de referencia, el estudio de las conformaciones que adoptan las macromoléculas al interaccionar de forma transitoria resulta considerablemente más complejo, con costes computacionales elevados. Esta dificultad radica en los numerosos grados de libertad implicados y en el gran número de átomos del sistema que pueden desplazarse. Por esta razón, los algoritmos de docking suelen emplear estrategias para optimizar recursos, como el uso de transformadas de Fourier en lugar del empleo explícito de matrices de rotación y traslación (Katchalski-Katzir et al. 1992).

Un subproblema específico lo constituye el acoplamiento entre una enzima y su sustrato, una tarea para la cual la información genómica (por ejemplo, la organización en operones) puede resultar especialmente valiosa (Zhao et al. 2013).

Además de los bancos de pruebas publicados por diversos desarrolladores (Yu and Guerois 2016), desde 2001 se desarrolla un experimento colectivo denominado CAPRI, en el que periódicamente se evalúan diferentes algoritmos para predecir, antes de su publicación, las conformaciones de complejos proteicos cuyas estructuras han sido resueltas experimentalmente (generalmente mediante cristalografía).

La lista de programas de acoplamiento molecular o docking es extensa, por lo que resulta recomendable consultar los resultados recientes de CAPRI para seleccionar el software más adecuado según las necesidades específicas. Un aspecto adicional a considerar es que estos programas están diseñados, por definición, para usuarios avanzados y requieren cierta experiencia, particularmente en la interpretación de los resultados.

Una forma accesible de iniciarse en el manejo de software de docking consiste en PyRosetta (Chaudhury, Lyskov, and Gray 2010). Este entorno permite realizar, de forma programática, una simulación de docking en miniatura. En el ejemplo propuesto se aborda el acoplamiento entre un dúplex de ADN y el factor de transcripción DnaA, un problema que puede plantearse simultáneamente como un caso clásico de docking y como un problema de especificidad de reconocimiento:

Como resultado de las simulaciones de docking se obtiene una serie de complejos, que pueden mostrar o no interfaces biológicamente relevantes, dependiendo de la profundidad del muestreo realizado y del análisis posterior de los resultados. Este análisis requiere cierta experiencia y, sobre todo, un conocimiento adecuado de las moléculas implicadas.

