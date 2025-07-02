# app.py
import streamlit as st
import tempfile, io
from contextlib import redirect_stdout
import miscript

st.set_page_config(page_title="Generador de Informes PDF")
st.title("⚒️ Generador Automatizado de Informes PDF")

# 1) Input: carpeta principal en el servidor
ruta = st.text_input("1. Ruta de la carpeta principal", placeholder=r"F:\ULMU-T6-0012-Chaktemal")

# 2) Input: subir el Excel que alimenta step4
excel = st.file_uploader("2. Sube tu archivo Excel (.xlsx)", type=["xlsx"])

# 3) Botón para ejecutar todo
if st.button("▶️ Ejecutar todos los pasos"):
    if not ruta or not excel:
        st.error("❌ Debes indicar la ruta y subir el Excel antes de ejecutar.")
    else:
        # Guardar el Excel en un archivo temporal
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        tmp.write(excel.read())
        tmp.close()
        miscript.EXCEL_PATH     = tmp.name
        miscript.RUTA_PRINCIPAL = ruta

        # Capturar la salida de print() y mostrarla en la UI
        buffer_stdout = io.StringIO()
        with redirect_stdout(buffer_stdout):
            miscript.main()

        st.text_area("📝 Registro de ejecución", buffer_stdout.getvalue(), height=400)
        st.success("✅ Proceso completado")
