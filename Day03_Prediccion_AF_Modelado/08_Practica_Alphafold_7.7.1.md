---
title: "Práctica: Ejercicio con AF2"
subtitle: "Día 03"
author: "Velazquez Aldrete Zyanya Valentina"
date: "18/02/2026"
---

## Modelado estructural y evaluación de calidad

Se seleccionó una secuencia de *colágeno de 80 aminoácidos* para el modelado estructural. La predicción de la estructura terciaria se realizó utilizando ColabFold, basado en el algoritmo desarrollado por DeepMind mediante el sistema AlphaFold en su versión alphafold2_ptm.

Se generaron cinco modelos estructurales, los cuales fueron clasificados según su valor de pLDDT. El modelo mejor rankeado presentó un pLDDT promedio de 78.3, indicando una confianza estructural moderada-alta. El análisis por residuo mostró que la región central de la proteína (aproximadamente residuos 35–75) presenta *valores superiores a 90*, lo que sugiere una predicción altamente confiable en dicha zona. En contraste, los extremos N- y C-terminal mostraron valores entre 45 y 60, lo que podría indicar regiones flexibles o parcialmente desordenadas.

El *valor pTM* del modelo seleccionado fue de *0.491*, lo que sugiere una calidad global moderada del plegamiento tridimensional. Este valor es consistente con proteínas de tamaño pequeño y con posibles regiones estructuralmente dinámicas.

Adicionalmente, el modelo fue evaluado mediante herramientas de validación estructural como el análisis de Ramachandran, observándose que la mayoría de los residuos se encuentran en regiones favorecidas del espacio conformacional, lo que respalda la calidad geométrica del modelo.

En conjunto, las métricas obtenidas indican que el modelo estructural predicho presenta una calidad adecuada para estudios exploratorios de estructura-función, aunque podrían existir regiones flexibles que requieran validación experimental adicional.