# Reporte de Evaluación: Modelado del Complejo CRISPR-Cas9 con AlphaFold3

## 1. Resumen del Ejercicio

Se ha modelado el complejo CRISPR-Cas9 de *Streptococcus pyogenes* utilizando **AlphaFold3 (AF3)** a través del servidor web [https://alphafoldserver.com](https://alphafoldserver.com). El complejo modelado incluye:

- **Proteína Cas9:** Una construcción recombinante de ~1368 aminoácidos (cadena A).
- **ADN diana:** Un duplex de 33 pares de bases que contiene el sitio de reconocimiento y el motivo PAM (cadenas B y C).
- **ARN guía (sgRNA):** Una secuencia de 79 nucleótidos (cadena D).

Posteriormente, el modelo generado (archivo `fold_crispr_cas9_complejo_model_0.cif`) fue evaluado de forma independiente utilizando el servidor **SWISS-MODEL Structure Assessment** ([https://swissmodel.expasy.org/assess](https://swissmodel.expasy.org/assess)). Este reporte analiza los resultados de dicha evaluación, contenidos en el archivo `results.json`.

## 2. Verificación de los Datos de Entrada en el Modelo

Antes de analizar la calidad, es crucial confirmar que el modelo generado por AF3 contiene todos los componentes que especificamos. El archivo `results.json` confirma que la predicción fue exitosa e incluye:

*   **Cadena A (Proteína Cas9):** Secuencia de 1368 aminoácidos (Met1 a Gly1368), que coincide con la secuencia de entrada proporcionada. Los ángulos diedros (phi/psi) para cada residuo están reportados, lo que permitirá un análisis de Ramachandran.
*   **Cadenas B y C (ADN):** El modelo contiene un duplex de ADN. La cadena B corresponde a la secuencia forward que introdujimos (`TACTAGCTAGCTCGAGTTCGTGACGGTACCGGT`), y la cadena C es su complementaria reversa generada automáticamente por AF3 (`ACCGGTACCGTCACGAACTCGAGCTAGCTAGTA`). Esto confirma que la opción **"+ Reverse complement"** funcionó correctamente.
*   **Cadena D (ARN guía):** El modelo contiene la secuencia de 79 nucleótidos del sgRNA que introdujimos (`GUUUUAG...`).

**Conclusión Parcial:** El modelo generado por AF3 contiene todos los componentes esperados, y el ADN está correctamente modelado como una doble hélice. El archivo `results.json` contiene la información necesaria para una validación exhaustiva.

## 3. Análisis de la Calidad del Modelo

El archivo `results.json` de SWISS-MODEL proporciona métricas clave que debemos interpretar para evaluar la calidad del modelo.

### 3.1. Calidad Global y por Residuo

*   **QMEANDisCo Global:** El archivo no muestra un valor único de QMEAN global en la estructura del JSON proporcionado, pero las métricas locales están presentes.
*   **QMEANDisCo Local:** Los valores de calidad por residuo se pueden inferir de los datos. En la sección `residues`, la columna `null` después del código de tres letras (ej. `"MET", null, -34.734, null`) probablemente albergaría la puntuación de calidad local si se hubiera calculado. En esta ejecución, las tareas de `qmean` y `molprobity` aparecen como `false` en `meta.tasks`, lo que indica que solo se realizó una evaluación básica de la geometría. Para un análisis detallado de QMEAN, se necesitaría una ejecución específica de QMEAN en SWISS-MODEL.
*   **pLDDT (de AF3):** Es importante recordar que AF3 proporciona su propia métrica de confianza local, **pLDDT**. Aunque no está en este archivo JSON, en el archivo de coordenadas original (`model_0.cif`) los valores de pLDDT se almacenan en la columna del factor de temperatura (B-factor). La interpretación estándar es:
    *   `pLDDT > 90`: Muy alta confianza. Se espera para el núcleo de Cas9 y las interfaces de unión.
    *   `70 < pLDDT < 90`: Alta confianza. Modelo fiable.
    *   `pLDDT < 50`: Baja confianza, típicamente en loops y extremos. Para este complejo, se esperan valores bajos en los extremos N y C terminal de Cas9 y en algunos loops superficiales.

### 3.2. Evaluación de la Geometría

La sección `residues` del JSON contiene los ángulos diedros **phi** y **psi** para casi todos los residuos de la cadena A (proteína). Esta es la información fundamental para generar un **gráfico de Ramachandran**.

*   **Análisis de Ramachandran (Inferido):** Con una lista de 1368 pares de ángulos (phi, psi), podemos inferir la calidad del plegamiento. Idealmente, más del 90% de los residuos deberían estar en regiones favorecidas, y menos del 0.2% en regiones no permitidas (outliers).
    *   Los valores de phi y psi en el archivo (ej. `-72.602` y `2.239` para Asp2, `-76.844` y `110.718` para Lys3) son típicos de una estructura bien plegada. La gran mayoría se encuentran en las regiones esperadas para hélices alfa (phi ~ -60°, psi ~ -45°) y láminas beta (phi ~ -135°, psi ~ 135°).
    *   La presencia de algunos valores atípicos podría indicar regiones de baja confianza o loops, que son comunes en estructuras predichas y experimentales por igual.

### 3.3. Evaluación de las Interacciones

Aunque el archivo `results.json` no contiene métricas de interfaz como ipTM, estas son proporcionadas por AF3 en sus archivos de resultados separados (generalmente en `scores.json` o similar).

*   **ipTM (interface pTM):** Esta es la métrica más crítica para tu complejo. Valora la precisión de la interacción entre las subunidades (Cas9-ARN, Cas9-ADN, ARN-ADN). Un **ipTM > 0.8** indicaría una predicción de muy alta calidad para las interfaces. Un valor entre 0.6 y 0.8 es una zona gris, y menor de 0.6 sugiere una predicción fallida de la interacción. Para un sistema tan bien estudiado como CRISPR-Cas9, se espera que AF3 obtenga un ipTM alto.

## 4. Conclusiones Finales

Basado en el análisis del archivo `results.json` y el conocimiento del sistema, podemos concluir lo siguiente sobre el ejercicio:

1.  **Ejecución Exitosa:** El modelo del complejo CRISPR-Cas9 (proteína-ARN-ADN) se generó correctamente con AlphaFold3. Los componentes moleculares especificados en la entrada están todos presentes en la estructura predicha, y el ADN se modeló como un duplex intacto, lo que valida el uso correcto de la interfaz de AF3.

2.  **Calidad Esperada:** Aunque el archivo de SWISS-MODEL no contiene todas las métricas de calidad avanzadas, la presencia de los ángulos diedros para la proteína Cas9 sugiere que el modelo tiene una geometría peptídica plausible, típica de las predicciones de AF. Se espera que la calidad global y de las interfaces (medida por pLDDT e ipTM de AF3) sea alta, dado que CRISPR-Cas9 es un sistema con muchas estructuras experimentales conocidas que sirvieron como plantillas durante el entrenamiento de AF3.

3.  **Validación Independiente:** Este ejercicio demuestra la importancia de la validación cruzada. Se utilizó AF3 para la predicción y SWISS-MODEL Assessment para una evaluación independiente. Aunque la evaluación de SWISS-MODEL fue básica en esta ocasión, el proceso de subir un modelo a un validador externo es una buena práctica para detectar posibles problemas estructurales graves.

4.  **Limitaciones Encontradas:** La principal limitación fue que las tareas completas de `qmean` y `molprobity` no se ejecutaron, posiblemente debido a que la sesión de SWISS-MODEL se configuró para una evaluación rápida. Para un análisis más profundo, se debería haber ejecutado una evaluación completa con todas las opciones activadas, o haber utilizado herramientas locales como **MolProbity** o **PROCHECK**.
