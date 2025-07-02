#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script único que ejecuta el siguiente flujo de trabajo:
1. Renombrar carpetas
2. Renombrar archivos PDF en la carpeta "Excavación" y "Registros únicos"
3. Mover archivos renombrados a "Excavación por ID Monumento"
4. Crear subcarpetas en "Excavación por ID Monumento" y "Registros únicos"
5. Encarpetar archivos en "Excavación por ID Monumento"  y "Registros únicos"
6. Verificar archivos en la carpeta principal
7. Crear subcarpeta "Introducción general" y mover el archivo "IntroduccionGeneral.pdf"
8. Buscar archivos PDF vacíos

IMPORTANTE:
-La carpeta principal se debe nombrar de la misma manera que la columna "Nombre Sitio" de la base de datos (excel)
- Solo se define la ruta principal una vez (variable RUTA_PRINCIPAL).
- A partir de RUTA_PRINCIPAL se construyen las rutas para cada paso.
"""

import os
import shutil
import pandas as pd
from collections import defaultdict
import PyPDF2
# =============================================================================
# DEFINICIÓN DE LA RUTA PRINCIPAL (única definición) y # RUTAS DE ARCHIVOS
# =============================================================================
RUTA_PRINCIPAL = None  # ruta base para procesar carpetas y PDFs
EXCEL_PATH     = None  # ruta al archivo Excel para step4

# =============================================================================
# Paso 1: RENOMBRAR CARPETAS
# =============================================================================
def step1_renombrar_carpetas():
    if not RUTA_PRINCIPAL:
        raise ValueError("RUTA_PRINCIPAL no está definida")
    print("\n--- Paso 1: Renombrar Carpetas ---")
    
    # Diccionario con los nombres actuales y sus respectivos cambios
    renombrar = {
        "Excavacion": "Excavación",
        "Prospeccion": "Prospección",
        "RegistroUnico": "Registros únicos",
        "Dibujos": "Dibujos arquitectónicos",
        "FichaDeExcavacion": "Ficha de excavación",
        "Introduccion": "Introducción",
        "RegistroDeCapas": "Registro de capas",
        "RegistroDeFotogrametria": "Registro de fotogrametría",
        "RegistroDeMaterialesArqueologicos": "Registro de materiales arqueológicos",
        "RegistrosArqueologicos": "Registros arqueológicos"
    }
    
    def renombrar_carpetas_en_ruta(ruta_base):
        for root, dirs, files in os.walk(ruta_base, topdown=False):
            for carpeta in dirs:
                ruta_actual = os.path.join(root, carpeta)
                nuevo_nombre = renombrar.get(carpeta, None)
                if nuevo_nombre:
                    ruta_nueva = os.path.join(root, nuevo_nombre)
                    if not os.path.exists(ruta_nueva):
                        os.rename(ruta_actual, ruta_nueva)
                        print(f"Renombrado: {ruta_actual} → {ruta_nueva}")
                    else:
                        print(f"❌ No se pudo renombrar {ruta_actual} porque {ruta_nueva} ya existe.")
    
    renombrar_carpetas_en_ruta(RUTA_PRINCIPAL)


# =============================================================================
# Paso 2: RENOMBRAR ARCHIVOS EN LA CARPETA "Excavación" Y "Registros únicos"
# =============================================================================
def step2_renombrar_archivos():
    if not RUTA_PRINCIPAL:
        raise ValueError("RUTA_PRINCIPAL no está definida")
    print("\n--- Paso 2: Renombrar Archivos PDF ---")

    # Define las rutas de ambas carpetas
    carpeta_excavacion = os.path.join(RUTA_PRINCIPAL, "Excavación")
    carpeta_registros_unicos = os.path.join(RUTA_PRINCIPAL, "Registros únicos")
    
    def rename_pdfs_in_subfolders(main_path):
        for root, dirs, files in os.walk(main_path):
            folder_name = os.path.basename(root)
            for file in files:
                if file.endswith(".pdf"):
                    old_path = os.path.join(root, file)
                    new_name = f"{os.path.splitext(file)[0]}_{folder_name}.pdf"
                    new_path = os.path.join(root, new_name)
                    # Renombra solo si aún no tiene el sufijo de la subcarpeta
                    if not file.endswith(f"_{folder_name}.pdf"):
                        os.rename(old_path, new_path)
                        print(f"✅ Renombrado: {file} → {new_name}")
                    else:
                        print(f"⚠️ Ya tiene el formato esperado: {file}")
    
    # Procesa la carpeta "Excavación"
    if os.path.exists(carpeta_excavacion):
        print(f"Procesando archivos en 'Excavación'...")
        rename_pdfs_in_subfolders(carpeta_excavacion)
    else:
        print(f"❌ La carpeta 'Excavación' no existe en {RUTA_PRINCIPAL}")
    
    # Procesa la carpeta "Registros únicos"
    if os.path.exists(carpeta_registros_unicos):
        print(f"Procesando archivos en 'Registros únicos'...")
        rename_pdfs_in_subfolders(carpeta_registros_unicos)
    else:
        print(f"❌ La carpeta 'Registros únicos' no existe en {RUTA_PRINCIPAL}")


# =============================================================================
# Paso 3: MOVER ARCHIVOS RENOMBRADOS A "Excavación por ID Monumento"
# =============================================================================
def step3_mover_archivos_renombrados():
    if not RUTA_PRINCIPAL:
        raise ValueError("RUTA_PRINCIPAL no está definida")
    print("\n--- Paso 3: Mover Archivos ---")
    
    # Parte 1: Mover archivos desde "Excavación" a "Excavación por ID Monumento"
    carpeta_excavacion = os.path.join(RUTA_PRINCIPAL, "Excavación")
    carpeta_destino = os.path.join(RUTA_PRINCIPAL, "Excavación por ID Monumento")
    os.makedirs(carpeta_destino, exist_ok=True)
    
    def move_pdfs(main_path, output_path):
        for root, dirs, files in os.walk(main_path):
            for file in files:
                if file.endswith(".pdf"):
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(output_path, file)
                    if os.path.exists(new_path):
                        print(f"⚠️ El archivo ya existe en {output_path}: {file}, se omite.")
                    else:
                        shutil.move(old_path, new_path)
                        print(f"✅ Movido: {file} → {output_path}")
    
    if os.path.exists(carpeta_excavacion):
        move_pdfs(carpeta_excavacion, carpeta_destino)
    else:
        print(f"❌ La carpeta 'Excavación' no existe en {RUTA_PRINCIPAL}")
    
    # Parte 2: Mover archivos de las subcarpetas de "Registros únicos" a la carpeta "Registros únicos" (limpiar subcarpetas)
    carpeta_registros_unicos = os.path.join(RUTA_PRINCIPAL, "Registros únicos")
    if os.path.exists(carpeta_registros_unicos):
        print(f"Procesando archivos en subcarpetas de 'Registros únicos'...")
        for root, dirs, files in os.walk(carpeta_registros_unicos):
            # Si estamos en la carpeta raíz, no se mueve nada
            if os.path.abspath(root) == os.path.abspath(carpeta_registros_unicos):
                continue
            for file in files:
                if file.endswith(".pdf"):
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(carpeta_registros_unicos, file)
                    if os.path.exists(new_path):
                        print(f"⚠️ El archivo ya existe en {carpeta_registros_unicos}: {file}, se omite.")
                    else:
                        shutil.move(old_path, new_path)
                        print(f"✅ Movido: {file} → {carpeta_registros_unicos}")
    else:
        print(f"❌ La carpeta 'Registros únicos' no existe en {RUTA_PRINCIPAL}")



# =============================================================================
# Paso 4: CREAR SUBCARPETAS EN "Excavación por ID Monumento" Y "Registros únicos"
# =============================================================================
import os
import pandas as pd

def step4_crear_subcarpetas():
    if not RUTA_PRINCIPAL or not EXCEL_PATH:
        raise ValueError("Debe definir RUTA_PRINCIPAL y EXCEL_PATH")
    print("\n--- Paso 4: Crear Subcarpetas desde Excel ---")
    df = pd.read_excel(EXCEL_PATH, engine='openpyxl', dtype=str).fillna("")
    sitio = os.path.basename(RUTA_PRINCIPAL)
    df = df[df["Nombre Sitio"] == sitio]

    handled_ids = set()       # Para no procesar dos veces un mismo ID base
    created_combos = set()    # Para no crear dos veces la misma combinación

    for _, row in df.iterrows():
        base_id = row["ID Monumento"].strip()

        # --- Condicional: si alguno de esos dos campos empieza con "A", OMITIMOS el base_id ---
        sup = row.get("Monumentos superiores", "").strip()
        assoc = row.get("Monumentos Asociados por cercanía", "").strip()
        include_base = not (sup.startswith("A") or assoc.startswith("A"))

        # Si no incluimos base_id y no hay otros T…, saltamos la fila
        other_ts = [row.get(col, "").strip() for col in ["Monumentos superiores", "Monumentos Asociados por cercanía"] if row.get(col, "").strip().startswith("T")]
        if not include_base and not other_ts:
            continue

        # Construir lista de IDs
        ids = set()
        if include_base:
            # sólo agregamos el ID propio si no empieza A en ninguno de los dos campos
            ids.add(base_id)

        for col in ["Monumentos superiores", "Monumentos Asociados por cercanía"]:
            val = row.get(col, "").strip()
            if val.startswith("T"):
                ids.add(val)

        # Si ya procesamos todos esos IDs, lo saltamos
        if ids & handled_ids:
            continue

        # Marcar todos como manejados
        handled_ids.update(ids)

        # Ordenar para evitar duplicados en distinto orden
        sorted_ids = sorted(ids)
        combo_key = tuple(sorted_ids)
        if combo_key in created_combos:
            continue
        created_combos.add(combo_key)

        # Nombre de carpeta
        folder_name = ", ".join(sorted_ids)

        # Elegir carpeta padre
        tipo = row.get("Tipo de intervención", "").strip()
        if tipo == "Excavación":
            base = os.path.join(RUTA_PRINCIPAL, "Excavación por ID Monumento")
        elif tipo == "Registro único":
            base = os.path.join(RUTA_PRINCIPAL, "Registros únicos")
        else:
            print(f"⚠️ Tipo desconocido '{tipo}' para ID {base_id}, se omite.")
            continue

        ruta_sub = os.path.join(base, folder_name)
        os.makedirs(ruta_sub, exist_ok=True)
        print(f"✅ Subcarpeta creada: {ruta_sub}")

# =============================================================================
# Paso 5: ENCARPETAR ARCHIVOS EN "Excavación por ID Monumento" Y "Registros únicos"
# =============================================================================
import os
import re
import shutil

def step5_encarpetar_archivos():
    if not RUTA_PRINCIPAL:
        raise ValueError("RUTA_PRINCIPAL no está definida")
    print("\n--- Paso 5: Encarpetar Archivos ---")
    carpeta_excavacion = os.path.join(RUTA_PRINCIPAL, "Excavación por ID Monumento")
    carpeta_registros = os.path.join(RUTA_PRINCIPAL, "Registros únicos")

    def procesar_carpeta(carpeta):
        print(f"\nProcesando en: {carpeta}")
        # 1) Construyo mapa identificador → ruta de subcarpeta
        mapa = {}
        for sub in os.listdir(carpeta):
            ruta_sub = os.path.join(carpeta, sub)
            if not os.path.isdir(ruta_sub):
                continue
            for id_ in [i.strip() for i in sub.split(",")]:
                if id_:
                    mapa[id_] = ruta_sub
        print(f"  Mapeados {len(mapa)} IDs a subcarpeta.")

        # 2) Recorrer PDFs en la raíz de 'carpeta'
        for nombre in os.listdir(carpeta):
            if not nombre.lower().endswith(".pdf"):
                continue
            ruta_pdf = os.path.join(carpeta, nombre)
            stem = os.path.splitext(nombre)[0]

            # Extraigo T##_##### aunque haya guiones bajos contiguos
            ids_en_nombre = re.findall(r"T\d+_\d+", stem)
            if not ids_en_nombre:
                print(f"⚠️ No hay IDs en '{nombre}', no se copia ni elimina.")
                continue

            # 3) Copiar a cada subcarpeta encontrada
            copiado_al_menos_una_vez = False
            for id_ in ids_en_nombre:
                if id_ in mapa:
                    destino = mapa[id_]
                    ruta_destino = os.path.join(destino, nombre)
                    if not os.path.exists(ruta_destino):
                        shutil.copy2(ruta_pdf, ruta_destino)
                        print(f"✅ Copiado: {nombre} → {destino}")
                    else:
                        print(f"⚠️ Ya existe en {destino}: {nombre}")
                    copiado_al_menos_una_vez = True
                else:
                    print(f"⚠️ Sin carpeta para ID '{id_}' (archivo {nombre})")

            # 4) Si al menos se copió una vez, elimino el original
            if copiado_al_menos_una_vez:
                try:
                    os.remove(ruta_pdf)
                    print(f"🗑️ Eliminado original: {ruta_pdf}")
                except Exception as e:
                    print(f"❌ No se pudo eliminar {ruta_pdf}: {e}")

    # Ejecutar en ambas carpetas si existen
    if os.path.isdir(carpeta_excavacion):
        procesar_carpeta(carpeta_excavacion)
    else:
        print(f"❌ No existe: {carpeta_excavacion}")

    if os.path.isdir(carpeta_registros):
        procesar_carpeta(carpeta_registros)
    else:
        print(f"❌ No existe: {carpeta_registros}")

    print("\n🎉 Paso 5 completado.")


# =============================================================================
# Paso 6: VERIFICACIÓN DE ARCHIVOS EN LA CARPETA PRINCIPAL
# =============================================================================
def step6_verificacion_archivos():
    if not RUTA_PRINCIPAL or not EXCEL_PATH:
        raise ValueError("Debe definir RUTA_PRINCIPAL y EXCEL_PATH")
    print("\n--- Paso 6: Verificación de Archivos ---")
    
    # Rutas para la verificación
    prospection_dir = os.path.join(RUTA_PRINCIPAL, "Prospección")
    excavation_id_dir = os.path.join(RUTA_PRINCIPAL, "Excavación por ID Monumento")
    registros_unicos_dir = os.path.join(RUTA_PRINCIPAL, "Registros únicos")
    
    expected_suffixes = [
        "Introducción.pdf",
        "Ficha de excavación.pdf",
        "Dibujos arquitectónicos.pdf",
        "Registro de capas.pdf",
        "Registro de fotogrametría.pdf",
        "Registro de materiales arqueológicos.pdf",
        "Registros arqueológicos.pdf"
    ]
    
    def verify_prospection_files(EXCEL_PATH):
        try:
            df = pd.read_excel(EXCEL_PATH, engine='openpyxl', dtype=str)
            if "ID Monumento" not in df.columns or "Nombre Sitio" not in df.columns:
                print("❌ El archivo Excel no contiene las columnas esperadas (ID Monumento y Nombre Sitio).")
                return
            # Se filtran los registros que correspondan al nombre de la carpeta principal
            df_filtered = df[df["Nombre Sitio"] == os.path.basename(RUTA_PRINCIPAL)]
            expected_files = set(df_filtered["ID Monumento"].dropna().astype(str) + ".pdf")
            existing_files = set(f for f in os.listdir(prospection_dir) if f.endswith(".pdf"))
            missing_files = expected_files - existing_files
            if missing_files:
                print("❌ Faltan archivos en Prospección:")
                for missing in missing_files:
                    print(f"   - {missing}")
            extra_files = existing_files - expected_files
            if extra_files:
                print("🚨 Archivos adicionales encontrados en Prospección:")
                for extra in extra_files:
                    print(f"   - {extra}")
            if not missing_files and not extra_files:
                print("✅ Todos los archivos esperados están en la carpeta Prospección.")
        except Exception as e:
            print(f"❌ Error al procesar el archivo Excel: {e}")
    
    # Ajusta la ruta del Excel según corresponda
    verify_prospection_files(EXCEL_PATH)
    
    
    # --- Archivos fuera de subcarpetas en Excavación por ID ---
    sueltos = [
        f for f in os.listdir(excavation_id_dir)
        if os.path.isfile(os.path.join(excavation_id_dir, f)) and f.lower().endswith(".pdf")
    ]
    if sueltos:
        print("🚨 Archivos fuera de subcarpetas encontrados en 'Excavación por ID Monumento':")
        for f in sueltos:
            print(f"   - {f}")
    else:
        print("✅ No hay archivos fuera de las subcarpetas en 'Excavación por ID Monumento'.")
    
    # --- Verificación dentro de cada subcarpeta ---
    for folder in os.listdir(excavation_id_dir):
        folder_path = os.path.join(excavation_id_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        
        print(f"\n🔍 Verificando carpeta: {folder}")
        found_files    = defaultdict(list)
        extra_files    = []
        files_in_folder = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
        
        # 1) Clasificar cada PDF según suffix
        for f in files_in_folder:
            matched = False
            for suffix in expected_suffixes:
                if f.endswith(suffix):
                    found_files[suffix].append(f)
                    matched = True
                    break
            if not matched:
                extra_files.append(f)
        
        # 2) Detectar faltantes
        missing = [s for s in expected_suffixes if s not in found_files]
        if missing:
            print("❌ Faltan archivos:")
            for m in missing:
                print(f"   - {m}")
        
        # 3) Detectar duplicados
        dupes = {s: lst for s, lst in found_files.items() if len(lst) > 1}
        if dupes:
            print("⚠️ Archivos duplicados encontrados:")
            for suf, lst in dupes.items():
                print(f"   - {suf}: {', '.join(lst)}")
        
        # 4) Detectar extras
        if extra_files:
            print("🚨 Archivos adicionales encontrados:")
            for e in extra_files:
                print(f"   - {e}")
        
        if not (missing or dupes or extra_files):
            print("✅ Todo está en orden en esta carpeta.")
    
    
    # VERIFICACIÓN PARA "REGISTROS ÚNICOS"
    print("\n--- Verificando la carpeta 'Registros únicos' ---")
    if os.path.exists(registros_unicos_dir):
        # 1. Verificar archivos PDF fuera de subcarpetas en "Registros únicos"
        archivos_sueltos = [f for f in os.listdir(registros_unicos_dir) 
                             if os.path.isfile(os.path.join(registros_unicos_dir, f)) and f.endswith(".pdf")]
        if archivos_sueltos:
            print("🚨 Archivos fuera de subcarpetas encontrados en 'Registros únicos':")
            for archivo in archivos_sueltos:
                print(f"   - {archivo}")
        else:
            print("✅ No hay archivos fuera de subcarpetas en 'Registros únicos'.")
        
        # 2. Verificar que cada subcarpeta cuyo nombre inicie con "T" tenga al menos un PDF
        for folder in os.listdir(registros_unicos_dir):
            folder_path = os.path.join(registros_unicos_dir, folder)
            if os.path.isdir(folder_path) and folder.startswith("T"):
                pdfs_en_folder = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
                if not pdfs_en_folder:
                    print(f"❌ ALERTA: La subcarpeta '{folder}' no contiene ningún documento PDF.")
                else:
                    print(f"✅ La subcarpeta '{folder}' tiene {len(pdfs_en_folder)} documento(s) PDF.")
    else:
        print(f"❌ La carpeta 'Registros únicos' no existe en {RUTA_PRINCIPAL}")
    
    print("\n🎉 Verificación completada en la carpeta principal.")

# =============================================================================
# Paso 7: CREAR SUBCARPETA "Introducción general" y MOVER el archivo "IntroduccionGeneral.pdf"
# =============================================================================
def step7_encarpetar_introduccion_general():
    if not RUTA_PRINCIPAL:
        raise ValueError("RUTA_PRINCIPAL no está definida")
    print("\n--- Paso 7: Encarpetar Introducción General ---")
    
    # Ruta del archivo "IntroduccionGeneral.pdf" en la carpeta principal
    archivo_introduccion = os.path.join(RUTA_PRINCIPAL, "IntroduccionGeneral.pdf")
    
    # Ruta de la subcarpeta "Introducción general" dentro de la carpeta principal
    carpeta_introduccion_general = os.path.join(RUTA_PRINCIPAL, "Introducción general")
    
    # Verificar si el archivo existe en la carpeta principal
    if os.path.exists(archivo_introduccion):
        # Crear la subcarpeta "Introducción general" si no existe
        os.makedirs(carpeta_introduccion_general, exist_ok=True)
        
        # Mover el archivo a la subcarpeta
        nuevo_destino = os.path.join(carpeta_introduccion_general, "IntroduccionGeneral.pdf")
        if os.path.exists(nuevo_destino):
            print(f"⚠️ El archivo ya existe en '{carpeta_introduccion_general}': IntroduccionGeneral.pdf")
        else:
            shutil.move(archivo_introduccion, nuevo_destino)
            print(f"✅ Movido 'IntroduccionGeneral.pdf' a '{carpeta_introduccion_general}'")
    else:
        print(f"❌ No se encontró 'IntroduccionGeneral.pdf' en {RUTA_PRINCIPAL}")

# =============================================================================
# Paso 8: BUSCAR ARCHIVOS PDF VACÍOS
# =============================================================================
def step8_buscar_pdfs_vacios():
    if not RUTA_PRINCIPAL:
        raise ValueError("RUTA_PRINCIPAL no está definida")
    print("\n--- Paso 8: Buscar PDFs Vacíos ---")
    """
    Determina si un PDF es vacío.
    Se considera vacío si el tamaño del archivo es 0 bytes o
    si al leerlo no se detectan páginas.
    """
    try:
        if os.path.getsize(ruta_pdf) == 0:
            return True
        with open(ruta_pdf, 'rb') as archivo:
            lector = PyPDF2.PdfReader(archivo)
            if len(lector.pages) == 0:
                return True
    except Exception as e:
        print(f"Error al leer {ruta_pdf}: {e}")
    return False

def buscar_pdfs_vacios(carpeta_raiz):
    """
    Recorre la carpeta y subcarpetas para encontrar archivos PDF vacíos.
    """
    pdfs_vacios = []
    for ruta_directorio, subdirectorios, archivos in os.walk(carpeta_raiz):
        for archivo in archivos:
            if archivo.lower().endswith('.pdf'):
                ruta_completa = os.path.join(ruta_directorio, archivo)
                if es_pdf_vacio(ruta_completa):
                    pdfs_vacios.append(ruta_completa)
    return pdfs_vacios

def step8_buscar_pdfs_vacios():
    print("\n--- Paso 8: Buscar PDFs Vacíos ---")
    pdfs_vacios = buscar_pdfs_vacios(RUTA_PRINCIPAL)
    if pdfs_vacios:
        print("Se encontraron los siguientes archivos PDF vacíos:")
        for ruta in pdfs_vacios:
            print(ruta)
    else:
        print("No se encontraron archivos PDF vacíos.")

# =============================================================================
# Función principal
# =============================================================================
def main():
    # Validar
    if RUTA_PRINCIPAL is None or EXCEL_PATH is None:
        raise ValueError("RUTA_PRINCIPAL y EXCEL_PATH deben asignarse antes de ejecutar main()")
    # Llamadas secuenciales
    step1_renombrar_carpetas()
    step2_renombrar_archivos()
    step3_mover_archivos_renombrados()
    step4_crear_subcarpetas()
    step5_encarpetar_archivos()
    step6_verificacion_archivos()
    step7_encarpetar_introduccion_general()
    step8_buscar_pdfs_vacios()
