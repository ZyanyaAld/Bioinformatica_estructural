# Resumen: Estructura Terciaria - Comparación de Proteínas

Este tema aborda la comparación de la estructura tridimensional (terciaria) de proteínas, un paso crucial ya que la estructura está más conservada que la secuencia y permite encontrar relaciones evolutivas remotas.

## 1. El Problema Fundamental
Dadas las coordenadas 3D de dos proteínas (A y B), queremos cuantificar su parecido estructural. La solución general es buscar las subestructuras más grandes (`subA`, `subB`) que, al superponerse, minimicen la distancia entre sus átomos equivalentes.

## 2. Algoritmos Clásicos para la Comparación
Existen diversas estrategias para calcular la similitud estructural:

*   **Foldseek / FoldMason:** Convierte la estructura 3D en una secuencia de un alfabeto estructural para acelerar la búsqueda y comparación.
*   **STAMP (Alignment-based):** Usa un proceso iterativo: 1) alinea con matrices de sustitución (ej. BLOSUM), 2) superpone las estructuras, 3) refina los residuos equivalentes basándose en umbrales de distancia. Repite hasta converger (minimizar RMSD).
*   **SSAP (Double Dynamic Programming):** Usa programación dinámica doble: primero identifica fragmentos localmente similares y luego encuentra el subconjunto óptimo de estos fragmentos para la superposición global.
*   **DALI (Distance Matrix Alignment):** Compara matrices de distancias (en lugar de coordenadas 3D). Convierte cada proteína en una matriz de distancias Cα-Cα y luego compara las matrices para encontrar la mejor alineación, lo que evita cálculos de rotación.
*   **MAMMOTH:** Un método destacado (pre-AlphaFold) que: 1) mide la similitud local de heptapéptidos, 2) alinea estas regiones, 3) encuentra el subconjunto máximo de Cα cercanos (<4Å), y 4) calcula un **E-value** (valor esperado) para evaluar la significancia estadística del alineamiento.
*   **mmligner:** Minimiza la información necesaria para reconstruir una estructura desde la otra, evitando umbrales subjetivos.

## 3. Estrategias de Superposición
La elección del método depende de si las proteínas tienen dominios múltiples o regiones variables:
*   **Rígida:** Busca un único alineamiento para toda la estructura (puede sacrificar residuos alineados o calidad del RMSD).
*   **Flexible:** Divide la estructura en subestructuras rígidas (ej. dominios) para optimizar el RMSD por partes.
*   **Elástica (basada en matrices de distancias):** Permite alinear dominios de forma independiente maximizando los residuos equivalentes.

![Tres estrategias de comparación estructural: rígida, flexible y elástica](figures/Structure.jpg)
*Figura 1. Tres estrategias (rígida, flexible y elástica) para comparar la estructura terciaria. Adaptada de Hasegawa and Holm (2009).*

## 4. Métricas de Similitud
El **RMSD** es la métrica clásica, pero tiene limitaciones (es sensible a outliers y a la longitud de la proteína). Por eso se han desarrollado otras:

*   **TM-score (Template Modeling score):** Es la métrica estándar actual. Ponderan las distancias para que desviaciones pequeñas en el *core* de la proteína tengan más peso que desviaciones grandes en *loops*. Valores > 0.5 indican el mismo plegamiento. Se calcula con herramientas como **TM-align**.
*   **lDDT (local Distance Difference Test):** Evalúa la distancia local entre átomos vecinos (sin necesidad de superposición previa). Se usa mucho en CASP para evaluar modelos.
*   **E-value (de MAMMOTH):** Similar al de BLAST, da una significancia estadística al parecido encontrado, superando la subjetividad del RMSD.

## 5. Consideraciones y Complejidades
*   **No hay una única respuesta "correcta":** No existe una definición universalmente aceptada del alineamiento estructural óptimo. Por eso hay tantos programas y cada usuario tiene su preferido.
*   **Taxonomías estructurales:** Clasificaciones como CATH o SCOP son muy útiles, pero la evolución de los plegamientos (folds) puede ser un proceso continuo y no siempre discreto. Aparecen conceptos como **permutaciones circulares**, donde el orden de los elementos de estructura secundaria puede estar reorganizado.
*   **Superfamilias y plegamientos:** Se acepta que una **superfamilia** agrupa estructuras muy similares (aunque la secuencia diverja) y un **plegamiento (fold)** agrupa superfamilias con la misma topología de estructura secundaria.

## 6. Aplicaciones Específicas: Factores de Transcripción
Un caso particular de comparación estructural es el estudio de dominios de unión a DNA (DBD):
*   **TFcompare:** Método especializado en superponer factores de transcripción para deducir el alineamiento correcto de sus sitios de unión (*cis*-elements).
*   **Mecanismos de reconocimiento:** La superposición estructural de DBDs revela que el mecanismo de reconocimiento del DNA no siempre está conservado, aunque la estructura global del dominio sí lo esté.

![Superposición de dominios de unión a DNA](figures/TF_compare.jpg)
*Figura 2. Superposiciones de dominios de unión a DNA (DBD) de factores de transcripción. Adaptada de Sebastian and Contreras-Moreira (2013).*

## 7. Taxonomías Estructurales y su Evolución
*   **CATH y SCOP:** Clasificaciones clásicas de dominios proteicos. Sin embargo, el texto menciona que los plegamientos (*folds*) pueden no ser entidades completamente discretas.
*   **SCOP2:** Surgió para superar las limitaciones de SCOP, reconociendo relaciones más complejas entre proteínas.
*   **Permutaciones circulares:** Un mismo plegamiento puede aparecer con el orden de los elementos de estructura secundaria reorganizado circularmente.
*   **TED (The Encyclopedia of Domains, 2024):** Proyecto reciente que amplía el repertorio de dominios conocidos aprovechando la explosión de datos de AlphaFold.

## 8. Comparación de Métodos y Benchmarking
*   **MAMMOTH vs. otros:** En su momento, MAMMOTH fue comparado con otros algoritmos e incluso con el criterio de expertos humanos (como Murzin), mostrando alta correlación con la evaluación visual.
*   **Criterio de experto humano:** La validación final de muchos algoritmos incluía la comparación con el juicio de expertos en estructura de proteínas.

![Comparación de métodos estructurales](figures/MAMMOTH_comparison.jpg)
*Figura 3. Semejanza de MAMMOTH respecto a otros algoritmos y al criterio de un experto humano. Adaptada de Ortiz, Strauss, and Olmea (2002).*

## 9. Alineamiento Estructural Múltiple
Los avances recientes apuntan a:
*   **FoldMason:** Herramientas como FoldMason (integrada en Foldseek) permiten alineamientos múltiples de estructuras, combinando información de secuencia y estructura.
*   **Clustering masivo:** Algoritmos para agrupar miles de estructuras de manera eficiente (Barrio-Hernandez et al. 2023).

### 10. Terminos Clave

| Término | Definición |
|---------|------------|
| **RMSD** | Root Mean Square Deviation. Desviación cuadrática media entre átomos equivalentes tras superponer dos estructuras. |
| **TM-score** | Métrica que pondera distancias para dar más importancia al core estructural. Valores >0.5 indican mismo plegamiento. |
| **lDDT** | Local Distance Difference Test. Evalúa distancias locales sin necesidad de superposición previa. |
| **E-value** | Valor esperado. Probabilidad de encontrar una similitud por azar. |
| **DBD** | DNA-Binding Domain. Dominio de unión a DNA. |
| **Fold** | Plegamiento. Topología global de la estructura secundaria. |
| **Superfamilia** | Grupo de proteínas con estructuras muy similares pero secuencia divergente. |

---

###  Referencias Clave 
Las referencias mencionadas en el texto que podrías añadir:
- Chothia and Lesk (1986) - EMBO J.
- Hasegawa and Holm (2009) - Curr. Opin. Struct. Biol.
- Ortiz, Strauss, and Olmea (2002) - Protein Science
- Zhang and Skolnick (2004, 2005) - Nucleic Acids Res. y Proteins
- Mariani et al. (2013) - Bioinformatics
- Lau et al. (2024) - TED: The Encyclopedia of Domains
