

# Práctica: Alineamiento Estructural, Superposición y Cálculo de RMSD / %Identidad

## 1. Instrucciones y Objetivos del Ejercicio

### Objetivos

El objetivo principal de esta práctica es aprender a realizar y analizar alineamientos estructurales de proteínas utilizando herramientas bioinformáticas disponibles en línea y scripts de procesamiento de datos. Al finalizar el ejercicio, serás capaz de:

1. **Seleccionar dominios proteicos relacionados** de una base de datos de clasificación estructural (CATH).
2. **Generar un alineamiento estructural múltiple** utilizando una herramienta web especializada (FoldMason).
3. **Visualizar e interpretar** los resultados de una superposición estructural, tanto gráficamente (superposición 3D) como en forma de alineamiento de secuencias.
4. **Calcular métricas cuantitativas** para evaluar la calidad de la superposición y la similitud entre pares de proteínas:
   - **RMSD (Root Mean Square Deviation):** Una medida de la distancia promedio entre los átomos de las proteínas superpuestas. Un RMSD bajo indica una alta similitud estructural.
   - **Porcentaje de Identidad:** Una medida de la similitud de secuencia en las regiones alineadas.
5. **Modificar y utilizar un script en Python** para procesar archivos estructurales y de secuencia, automatizando los cálculos.

### Instrucciones del Ejercicio

El flujo de trabajo a seguir es el siguiente:

1. **Selección de Dominios:** Visita la base de datos CATH y busca un dominio, por ejemplo, 'homeodomain'. Selecciona un grupo de 5 a 10 dominios relacionados. Anota sus códigos (ej. `3lnqA00` corresponde a la estructura 3LNQ del PDB, cadena A).
2. **Alineamiento Estructural con FoldMason:** Accede al servidor web FoldSeek FoldMason. Introduce los códigos de los dominios seleccionados y ejecuta el alineamiento.
3. **Descarga de Resultados:** Una vez finalizado el proceso, descarga los resultados en los siguientes formatos:
   - `.png`: Una imagen de la superposición estructural.
   - `.pdb`: Un archivo con las coordenadas de todas las estructuras superpuestas.
   - `.fasta`: El alineamiento múltiple de secuencias correspondiente.
   - También guarda una captura de pantalla del alineamiento múltiple de secuencias tal como se muestra en la web.
4. **Resumen de Resultados:** Utiliza la función de envío de resultados a FoldSeek (el botón al pie de la página). Resume la información proporcionada en una tabla.
5. **Cálculo de Métricas por Pares:** Utilizando los archivos descargados y modificando el script proporcionado, calcula el porcentaje de identidad y el RMSD para un conjunto de pares de estructuras. Resume estos resultados en una tabla final.

---

## 2. Resolución del Ejercicio

En esta sección se detalla el proceso paso a paso para completar la práctica, utilizando los datos y herramientas proporcionados.

### 2.1. Selección de Dominios y Obtención de Resultados de FoldMason

Para este ejercicio, se seleccionaron las siguientes estructuras de la base de datos CATH/PDB:

| ID en FoldMason | Descripción |
|:---|:---|
| 3BK1cif | Cadena A de la estructura 3BK1 |
| 3BK2cif | Cadena A de la estructura 3BK2 |
| 3BC2cif | Cadena A de la estructura 3BC2 |
| 3BV6cif_C | Cadena C de la estructura 3BV6 |
| 3BECcif | Cadena A de la estructura 3BEC |
| 3BLMcif | Cadena A de la estructura 3BLM |
| 3BEBcif | Cadena A de la estructura 3BEB |
| 3BV6cif_A | Cadena A de la estructura 3BV6 |
| 3BV6cif_B | Cadena B de la estructura 3BV6 |
| 3BV6cif_D | Cadena D de la estructura 3BV6 |
| 3BV6cif_E | Cadena E de la estructura 3BV6 |
| 3BV6cif_F | Cadena F de la estructura 3BV6 |

Estos IDs se introdujeron en el servidor FoldMason ([https://search.foldseek.com/foldmason](https://search.foldseek.com/foldmason)) para generar un alineamiento estructural múltiple.

**Resultados descargados:**
- `foldmason.png`: Imagen de la superposición estructural.
- `foldmason.pdb`: Archivo con las coordenadas 3D de todas las estructuras superpuestas en un mismo sistema de referencia.
- `foldmason_aa.fa`: Alineamiento múltiple de secuencias en formato FASTA (se muestra parcialmente a continuación).


### 2.2 Cálculo de % Identidad y RMSD por Pares

El script `prog3.1.py` está diseñado para superponer dos estructuras basándose en un alineamiento proporcionado y calcular el RMSD. Para este ejercicio, lo hemos adaptado para leer el alineamiento múltiple (`foldmason_aa.fa`) y calcular las métricas para pares de proteínas de nuestro interés.



## 3 Materiales y Archivos del Proyecto

**Archivos principales**  
- **`datos/foldmason_aa.fa`** — alineamiento múltiple FASTA (entrada de secuencias).  
- **`datos/foldmason.pdb`** — PDB combinado con coordenadas superpuestas (entrada de coordenadas).  
- **`codigo/download_and_merge_pdbs.py`** — script para obtener/combinar PDBs y generar `datos/foldmason.pdb`.  
- **`codigo/analisis.py`** — script que calcula % identidad y RMSD por pares; sobrescribe `resultados/pairwise_metrics.csv`.  
- **`resultados/pairwise_metrics.csv`** — salida tabular con métricas por pares (se sobrescribe en cada ejecución).  
- **`figuras/`** — imágenes descargadas de FoldMason (superposición, capturas del alineamiento).

**Nota**  
Dentro de cada archivo de código hay documentación y comentarios que explican el formato esperado de headers FASTA, el mapeo FASTA↔PDB y las funciones de extracción de coordenadas CA.
---

## 4 Preparación y Paso Previo Obligatorio

**Por qué es necesario**  
Si `datos/foldmason.pdb` no contiene todas las cadenas listadas en `foldmason_aa.fa`, `analisis.py` omitirá entradas. Para evitarlo hay que generar un PDB combinado que incluya todas las estructuras y que tenga antes de cada bloque ATOM la línea `REMARK    Name: <ID>`.

**Qué ejecutar antes del análisis**  
Desde la raíz del proyecto, ejecutar el script que descarga o extrae y combina los PDBs:

```bash
# colocarse siempre en la carpeta raiz de las subcarpetas del proyecto, en este caso Day02
cd "...\Day02_EstructuraTerciaria"
python codigo\download_and_merge_pdbs.py
```

**Resultado del paso previo**  
- Se crea o actualiza `datos/foldmason.pdb` con bloques ATOM precedidos por `REMARK    Name: <ID>`.  
- Con esto `analisis.py` podrá mapear correctamente cada header del FASTA a su bloque de coordenadas en el PDB combinado.

---

## 5 Ejecución del Análisis

**Comandos mínimos**  
Ejecutar el análisis principal después de completar el paso previo:

```bash
# ejecutar el análisis que calcula % identidad y RMSD
python codigo\analisis.py

# ver primeras líneas del CSV resultante
Get-Content resultados\pairwise_metrics.csv -TotalCount 20
```

**Comportamiento del script**  
- `analisis.py` lee `datos/foldmason_aa.fa` y `datos/foldmason.pdb`.  
- Calcula **% identidad** sobre posiciones sin gaps del alineamiento.  
- Extrae coordenadas **CA** de residuos alineados y calcula **RMSD** por pares.  
- **Sobrescribe** `resultados/pairwise_metrics.csv` en cada ejecución.

---

## 6 Resultados Tabla Resumen

**Tabla extraída de `resultados/pairwise_metrics.csv`**

| **ID1** | **ID2** | **% Identidad** | **NumCompared** | **RMSD (Å)** | **NumCoordsUsed** |
|---|---:|---:|---:|---:|---:|
| 3BK1cif | 3BK2cif | 99.82 | 549 | 78.278 | 549 |
| 3BK1cif | 3BC2cif | 11.82 | 203 | 61.630 | 203 |
| 3BK1cif | 3BV6cif_C | 12.24 | 286 | 90.111 | 286 |
| 3BK2cif | 3BV6cif_C | 11.97 | 284 | 69.900 | 284 |
| 3BECcif | 3BEBcif | 100.00 | 340 | 0.448 | 340 |
| 3BV6cif_A | 3BV6cif_B | 100.00 | 353 | 5.931 | 353 |

---

## 7 Interpretación y Notas Finales

**Interpretación breve**  
- **% Identidad**: calculada sobre posiciones sin gaps; valores altos indican conservación de secuencia en las regiones alineadas.  
- **RMSD**: calculado sobre átomos **CA** de residuos alineados; valores bajos indican superposición estructural cercana. Valores muy altos pueden indicar diferencias conformacionales, errores de mapeo o que las estructuras no son homólogas en la región alineada.  

**Observaciones prácticas**  
- El paso previo de combinación de PDBs es **obligatorio** cuando el PDB inicial no contiene todas las cadenas del FASTA.  
- `resultados/pairwise_metrics.csv` se **sobrescribe** en cada ejecución para mantener coherencia entre consola y archivo.  
- Si se desea recalcular la mejor superposición (Kabsch) antes de RMSD, el script puede ampliarse; la documentación para hacerlo está comentada en `codigo/analisis.py`.

---

### Comandos de referencia rápida

```bash
cd "...\Day02_EstructuraTerciaria"  #Colocarse siempre en la carpeta base del proyecto
python codigo\download_and_merge_pdbs.py
python codigo\analisis.py
Get-Content resultados\pairwise_metrics.csv -TotalCount 20
```

---
