import streamlit as st
import os
import sys
import subprocess

def get_resource_path(relative_path):
    """Obtiene la ruta del archivo de recursos, considerando si se está ejecutando desde un ejecutable empaquetado."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_executable_directory():
    """Obtiene la dirección del archivo que se está ejecutando"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def execute_command(nro_boton):
    archivo = get_resource_path(
        os.path.join("Procedures", diccionario_botones[nro_boton][0])
    )
    subprocess.Popen(
        ["python", archivo, "--theme", current_theme]
    )

# -------------------
# Theme
# -------------------
light_bg_color = "#ffffff"
dark_bg_color = "#313131"
light_fg_color = "#313131"
dark_fg_color = "#eeeeee"

# Set initial theme and background color
current_theme = st.selectbox("Choose theme:", ["dark", "light"])
bg_color = dark_bg_color if current_theme == "dark" else light_bg_color
fg_color = dark_fg_color if current_theme == "dark" else light_fg_color

# -------------------
# Diccionario Botones
# -------------------
diccionario_botones = {
    1: ("conciliadorArchivos.pyw", "Conciliador de archivos"),
    2: ("removerGuionesPuntos.pyw", "Remueve guiones y puntos"),
    3: ("TBD - archivo3.py", "TBD - nombre proceso 3"),
    4: ("TBD - archivo4.py", "TBD - nombre proceso 4"),
    5: ("TBD - archivo5.py", "TBD - nombre proceso 5"),
    6: ("TBD - archivo6.py", "TBD - nombre proceso 6"),
}

# -------------------
# Lista de Procesos Disponibles
# -------------------
procesos_disponibles = {
    "conciliadorArchivos.pyw": "Conciliador de archivos",
    "removerGuionesPuntos.pyw": "Remueve guiones y puntos",
    "TBD - archivo3.py": "TBD - nombre proceso 3",
    "TBD - archivo4.py": "TBD - nombre proceso 4",
    "TBD - archivo5.py": "TBD - nombre proceso 5",
    "TBD - archivo6.py": "TBD - nombre proceso 6",
}

# -------------------
# UI
# -------------------
st.title("Botonera Operativa")

st.write(f"<div style='background-color:{bg_color};color:{fg_color};padding:10px;border-radius:5px;'>", unsafe_allow_html=True)

# Mostrar botones
for i in range(1, 7):
    if st.button(diccionario_botones[i][1]):
        execute_command(i)

# Modo de edición
edit_mode = st.checkbox("Editar botones")

if edit_mode:
    st.write("Edit mode enabled. Select new processes for buttons:")
    for i in range(1, 7):
        new_process = st.selectbox(f"Botón {i}", list(procesos_disponibles.values()), index=list(procesos_disponibles.values()).index(diccionario_botones[i][1]))
        if new_process != diccionario_botones[i][1]:
            nuevo_archivo = [k for k, v in procesos_disponibles.items() if v == new_process][0]
            diccionario_botones[i] = (nuevo_archivo, new_process)

    if st.button("Aceptar"):
        st.success("Changes have been saved!")

st.write("</div>", unsafe_allow_html=True)