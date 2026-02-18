#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prog3.1 Calcula la superposicion en 3D equivalente a un alineamiento de 
secuencia de dos proteinas del PDB. Genera un fichero PDB con la superposicion 
obtenida. """
from __future__ import print_function

__author__  = 'Bruno Contreras-Moreira' 
__editor__   = 'Yeimi Gissel Contreras' 'Zyanya Valentina Vazquez'

from math import sqrt
import os
import csv

# Rutas (ajustar según tu estructura de archivos)
PDB_FILE = os.path.join("datos", "foldmason.pdb")
FASTA_FILE = os.path.join("datos", "foldmason_aa.fa")
OUT_CSV = os.path.join("resultados", "pairwise_metrics.csv")
# --- Escritura del CSV (sobrescribe cada ejecución por si las dudas jajasj saludos) ---

# Asegurarse de que la carpeta resultados existe antes de escribir el CSV
# os.makedirs("resultados", exist_ok=True)
# OUT_CSV = os.path.join("resultados", "pairwise_metrics.csv")

# -------------------------
# Lectura PDB por "cadena"
# -------------------------
def lee_coordenadas_PDB_por_cadena(filename):
    """
    Lee un PDB y devuelve dict {id_cadena: [res_block1, res_block2, ...]}
    Cada res_block es el conjunto de líneas ATOM pertenecientes a ese residuo.
    Soporta REMARK    Name: como identificador; si no existe, usa chain id (col 22).
    """
    coords_por_cadena = {}
    with open(filename, 'r') as pdbfile:
        cadena_actual = None
        coords_cadena_actual = []
        res_block = ''
        prev_resID = None

        for line in pdbfile:
            if line.startswith('REMARK') and 'Name:' in line:
                # guardar cadena anterior
                if cadena_actual and coords_cadena_actual:
                    coords_por_cadena[cadena_actual] = coords_cadena_actual
                cadena_actual = line.split('Name:')[1].strip()
                coords_cadena_actual = []
                res_block = ''
                prev_resID = None
                continue

            if line.startswith('ATOM') or line.startswith('HETATM'):
                # identificar residuo por (chain + resseq + icode)
                chain_id = line[21]
                resseq = line[22:26].strip()
                icode = line[26].strip()
                resID = f"{chain_id}:{resseq}{icode}"

                if prev_resID is None:
                    prev_resID = resID
                    res_block = line
                elif resID != prev_resID:
                    # guardar residuo anterior
                    if cadena_actual is None:
                        # fallback: usar chain id como nombre de cadena
                        cadena_actual = f"{prev_resID.split(':')[0]}"
                        if cadena_actual not in coords_por_cadena:
                            coords_por_cadena[cadena_actual] = []
                            # si había acumulado coords_cadena_actual, añadirlas
                    # append res_block to coords_cadena_actual
                    coords_cadena_actual.append(res_block)
                    # iniciar nuevo residuo
                    res_block = line
                    prev_resID = resID
                else:
                    res_block += line
            elif line.startswith('TER'):
                if res_block:
                    coords_cadena_actual.append(res_block)
                    res_block = ''
                # no cerrar cadena aquí: REMARK Name es preferible
                prev_resID = None
            else:
                continue

        # al final del archivo, guardar último residuo y cadena
        if res_block:
            coords_cadena_actual.append(res_block)
        if cadena_actual and coords_cadena_actual:
            coords_por_cadena[cadena_actual] = coords_cadena_actual
        else:
            # si no se detectó REMARK Name, intentar agrupar por chain en coords_por_cadena
            if not coords_por_cadena and coords_cadena_actual:
                # intentar inferir chain desde los bloques guardados
                coords_por_cadena["A"] = coords_cadena_actual

    return coords_por_cadena

# -------------------------
# Lectura FASTA alineado
# -------------------------
def lee_alineamiento_fasta(filename):
    secuencias = {}
    with open(filename, 'r') as f:
        id_actual = ''
        seq_actual = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if id_actual:
                    secuencias[id_actual] = ''.join(seq_actual)
                # tomar el primer token del header
                id_actual = line[1:].split()[0]
                seq_actual = []
            else:
                seq_actual.append(line)
        if id_actual:
            secuencias[id_actual] = ''.join(seq_actual)
    return secuencias

# -------------------------
# Extraer coordenadas CA
# -------------------------
def extrae_coords_atomo(res_block, atomo_seleccion=' CA '):
    for atomo in res_block.splitlines():
        if len(atomo) > 16 and atomo[12:16] == atomo_seleccion:
            try:
                return [float(atomo[30:38]), float(atomo[38:46]), float(atomo[46:54])]
            except:
                return None
    return None

# -------------------------
# Extraer pares alineados
# -------------------------
def extrae_pares_alineados(seq1, coords_list1, seq2, coords_list2):
    coords1_aln = []
    coords2_aln = []
    idx1, idx2 = 0, 0

    L = len(seq1)
    for i in range(L):
        res1 = seq1[i]
        res2 = seq2[i]

        if res1 != '-':
            # residuo presente en prot1
            if res2 != '-':
                # residuo presente en prot2 -> par alineado
                coord1 = extrae_coords_atomo(coords_list1[idx1]) if idx1 < len(coords_list1) else None
                coord2 = extrae_coords_atomo(coords_list2[idx2]) if idx2 < len(coords_list2) else None
                if coord1 and coord2:
                    coords1_aln.append(coord1)
                    coords2_aln.append(coord2)
                idx2 += 1
            idx1 += 1
        elif res2 != '-':
            idx2 += 1

    return coords1_aln, coords2_aln, len(coords1_aln)

# -------------------------
# Identidad y RMSD
# -------------------------
def calcular_identidad(seq1, seq2):
    matches = 0
    total = 0
    for a, b in zip(seq1, seq2):
        if a != '-' and b != '-':
            total += 1
            if a == b:
                matches += 1
    if total == 0:
        return 0.0, 0
    return (matches / total) * 100.0, total

def calcular_rmsd_simple(coords1, coords2):
    if len(coords1) != len(coords2) or len(coords1) == 0:
        return float('inf')
    suma = 0.0
    for c1, c2 in zip(coords1, coords2):
        dx = c1[0] - c2[0]
        dy = c1[1] - c2[1]
        dz = c1[2] - c2[2]
        suma += dx*dx + dy*dy + dz*dz
    return sqrt(suma / len(coords1))

# -------------------------
# Programa principal
# -------------------------
def main():
    os.makedirs("resultados", exist_ok=True)

    print("# Leyendo PDB:", PDB_FILE)
    coords_por_cadena = lee_coordenadas_PDB_por_cadena(PDB_FILE)
    print("# Cadenas encontradas en PDB:", list(coords_por_cadena.keys()))

    print("# Leyendo FASTA:", FASTA_FILE)
    secuencias = lee_alineamiento_fasta(FASTA_FILE)
    print("# Secuencias encontradas:", list(secuencias.keys()))

    ids_comunes = set(secuencias.keys()) & set(coords_por_cadena.keys())
    print("# IDs comunes (coordenadas y secuencia):", ids_comunes)

    if not ids_comunes:
        print("\n# ERROR: No hay coincidencia entre IDs del PDB y FASTA")
        print("# Revisa los headers del FASTA y los 'REMARK Name:' o chain ids en el PDB")
        return

    # pares a analizar (ajusta según tus intereses al analizar)
    pares = [
        ("3BK1cif", "3BK2cif"),
        ("3BK1cif", "3BC2cif"),
        ("3BK1cif", "3BV6cif_C"),
        ("3BK2cif", "3BV6cif_C"),
        ("3BECcif", "3BEBcif"),
        ("3BV6cif_A", "3BV6cif_B"),
    ]

    resultados = []
    with open(OUT_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID1", "ID2", "PercentIdentity", "NumCompared", "RMSD_A", "NumCoordsUsed"])
        for prot1, prot2 in pares:
            print(f"# Procesando: {prot1} vs {prot2}")
            if prot1 not in secuencias or prot2 not in secuencias:
                print("#  ERROR: Secuencia no encontrada en FASTA")
                continue
            if prot1 not in coords_por_cadena or prot2 not in coords_por_cadena:
                print("#  ERROR: Coordenadas no encontradas en PDB")
                continue

            seq1 = secuencias[prot1]
            seq2 = secuencias[prot2]
            coords1 = coords_por_cadena[prot1]
            coords2 = coords_por_cadena[prot2]

            if len(seq1) != len(seq2):
                print("#  ERROR: Longitudes de secuencia diferentes")
                continue

            identidad, compared = calcular_identidad(seq1, seq2)
            coords1_aln, coords2_aln, num_res = extrae_pares_alineados(seq1, coords1, seq2, coords2)

            if num_res > 0:
                rmsd = calcular_rmsd_simple(coords1_aln, coords2_aln)
                rmsd_str = f"{rmsd:.3f}"
                print(f"#  OK: {num_res} residuos alineados, RMSD={rmsd:.2f}Å, ID={identidad:.1f}%")
            else:
                rmsd = float('inf')
                rmsd_str = "N/D"
                print("#  WARN: No hay residuos alineados con coordenadas CA")

            writer.writerow([prot1, prot2, f"{identidad:.2f}", compared, rmsd_str, num_res])
            resultados.append((prot1, prot2, identidad, compared, rmsd, num_res))

# -------------------------
# Manejo de resultados y salida
# -------------------------
    with open(OUT_CSV, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID1", "ID2", "PercentIdentity", "NumCompared", "RMSD_A", "NumCoordsUsed"])
    for r in resultados:
        # si resultados es lista de diccionarios con 'par','identidad','rmsd','n_residuos'
        if isinstance(r, dict):
            id1, id2 = r['par'].split(' - ')
            identidad = r.get('identidad', 0.0)
            rmsd = r.get('rmsd', float('inf'))
            nres = r.get('n_residuos', 0)
            compared = r.get('num_compared', '')
        else:
            # si resultados es lista de tuplas (id1,id2,identidad,compared,rmsd,nres)
            id1 = r[0]; id2 = r[1]
            identidad = r[2] if len(r) > 2 else 0.0
            compared = r[3] if len(r) > 3 else ''
            rmsd = r[4] if len(r) > 4 else float('inf')
            nres = r[5] if len(r) > 5 else 0

        rmsd_str = "N/D" if rmsd == float('inf') else f"{float(rmsd):.6f}"
        writer.writerow([id1, id2, f"{float(identidad):.2f}", compared, rmsd_str, nres])
    print("\n# Resultados guardados en", OUT_CSV)

    # Mostrar tabla resumen en consola
    print("\n| Par | % Identidad | RMSD (Å) | Residuos alineados |")
    print("|:---|:---:|:---:|:---:|")
    for r in resultados:
        rmsd_disp = "N/D" if r[4] == float('inf') else f"{r[4]:.2f}"
        print(f"| {r[0]} - {r[1]} | {r[2]:.1f} | {rmsd_disp} | {r[5]} |")


        

if __name__ == "__main__":
    main()