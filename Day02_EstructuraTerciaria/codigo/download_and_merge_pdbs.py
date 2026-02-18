#!/usr/bin/env python3
# codigo/download_and_merge_pdbs.py

"""
download_and_merge_pdbs.py
----------------------------------------
Función principal
  - Descargar y combinar archivos PDB individuales correspondientes a los
    headers presentes en un alineamiento FASTA generado por FoldMason.
  - Genera un único PDB combinado (datos/foldmason.pdb) donde cada bloque
    ATOM está precedido por una línea:
        REMARK    Name: <HEADER>
    Esto permite que scripts posteriores (p. ej. analisis.py) mapeen cada
    bloque de coordenadas a su identificador de FASTA y calculen RMSD/%ID.

Cuándo ejecutarlo
  - Ejecutar **antes** de correr el análisis principal (codigo/analisis.py)
    cuando el PDB original no contiene todas las cadenas listadas en
    datos/foldmason_aa.fa.
  - Flujo recomendado:
      1) Extraer/colocar los archivos de FoldMason en datos/ o dejar el FASTA.
      2) Ejecutar este script para descargar/combinar PDBs:
         python codigo/download_and_merge_pdbs.py
      3) Ejecutar el análisis:
         python codigo/analisis.py

Requisitos
  - Python 3.x
  - Paquete Python: requests
    (instalar con: pip install requests)
  - Permiso de escritura en la carpeta datos/

Autores
  - Contreras Cornejo Yeimi Gissel
  - Velázquez Aldrete Zyanya Valentina
   
4to Semestre, Licenciatura en Ciencias Genómicas
Universidad Nacional Autónoma de México
Año 2026

Licencia / Uso
  - Uso académico y educativo. Incluir referencia a las autoras si se reutiliza
    el script en trabajos o informes.

Ejemplo de uso rápido (PowerShell)
  cd "C:\ruta\a\tu\proyecto"
  python codigo\download_and_merge_pdbs.py
"""


import os
import requests

FASTA = os.path.join("datos", "foldmason_aa.fa")
OUT_DIR = os.path.join("datos", "pdb_by_header")
MERGED_PDB = os.path.join("datos", "foldmason.pdb")

os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------
# Lectura de headers del FASTA
# Qué hace: lee datos/foldmason_aa.fa y extrae los identificadores
# Cuándo ejecutarlo: siempre, al inicio del script
# Funciones incluidas: extracción del primer token de cada línea '>'
# Salida: lista 'headers' con los identificadores en el mismo orden del FASTA
# ---------------------------------------------------------------------

headers = []
with open(FASTA, "r") as fh:
    for line in fh:
        if line.startswith(">"):
            hdr = line[1:].strip().split()[0]
            headers.append(hdr)

print(f"Encontrados {len(headers)} headers en {FASTA}")

# ---------------------------------------------------------------------
# Descarga de PDBs desde RCSB
# Qué hace: para cada header intenta inferir el PDB id (primeros 4 chars)
#           y descarga https://files.rcsb.org/download/<pdb_id>.pdb
# Cuándo ejecutarlo: después de leer los headers
# Funciones incluidas: descarga con requests, guardado en datos/pdb_by_header/
# Salida: archivos datos/pdb_by_header/<HEADER>.pdb (si disponibles)
# Nota: si ya existe el archivo, se reutiliza y no se vuelve a descargar
# ---------------------------------------------------------------------

downloaded = []
for hdr in headers:
    pdb_id = hdr[:4].lower()  # ej. '3bk1'
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    out_path = os.path.join(OUT_DIR, f"{hdr}.pdb")
    if os.path.exists(out_path):
        print(f"Ya existe {out_path}, saltando")
        downloaded.append(out_path)
        continue
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200 and "ATOM" in r.text:
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(r.text)
            print(f"Descargado {pdb_id} -> {out_path}")
            downloaded.append(out_path)
        else:
            print(f"NO DISPONIBLE en RCSB: {pdb_id} (HTTP {r.status_code})")
    except Exception as e:
        print(f"Error descargando {pdb_id}: {e}")

# ---------------------------------------------------------------------
# Merge / combinación de PDBs
# Qué hace: recorre los headers en el orden del FASTA y para cada PDB
#           existente escribe:
#               REMARK    Name: <HEADER>
#               <contenido del PDB>
#               TER
# Cuándo ejecutarlo: después de descargar/examinar los PDBs
# Funciones incluidas: apertura secuencial de archivos y escritura del PDB combinado
# Salida: datos/foldmason.pdb listo para el análisis estructural
# ---------------------------------------------------------------------

with open(MERGED_PDB, "w", encoding="utf-8") as out:
    for hdr in headers:
        pdb_file = os.path.join(OUT_DIR, f"{hdr}.pdb")
        if not os.path.exists(pdb_file):
            print(f"Advertencia: no existe {pdb_file}, se omitirá")
            continue
        out.write(f"REMARK    Name: {hdr}\n")
        with open(pdb_file, "r", encoding="utf-8") as pf:
            for line in pf:
                out.write(line)
        out.write("TER\n")


# ---------------------------------------------------------------------
# Salida y recomendaciones
# ---------------------------------------------------------------------
print("\nResumen:")
print(f"  FASTA usado: {FASTA}")
print(f"  PDBs descargados en: {OUT_DIR} (si estuvieron disponibles)")
print(f"  PDB combinado generado: {MERGED_PDB}")
print("\nSiguiente paso recomendado:")
print("  Ejecutar: python codigo\\analisis.py  (analisis.py usará datos/foldmason.pdb y datos/foldmason_aa.fa)")



print("Merge completado en:", MERGED_PDB)