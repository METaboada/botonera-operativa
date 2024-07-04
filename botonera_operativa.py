import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import subprocess

def get_resource_path(relative_path):
    """Obtiene la ruta del archivo de recursos, considerando si se está ejecutando desde un ejecutable empaquetado."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_executable_directory():
    """Obtiene la dirección del archivo que se está ejecutando
    Returns:
        _type_: Nombre del directorio en que se está ejecutando el código
    """
    if getattr(sys, "frozen", False):
        # Modo ejecutable (compilado)
        return os.path.dirname(sys.executable)
    else:
        # Modo script (desarrollo)
        return os.path.dirname(os.path.abspath(__file__))

def execute_command(nro_boton):
    archivo = get_resource_path(
        os.path.join("Procedures", diccionario_botones[nro_boton][0])
    )
    subprocess.Popen(
        ["python", archivo, "--theme", current_theme],
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

def toggle_mode():
    """Cambia el estilo de la aplicación entre light y dark mode"""
    global current_theme  # Acceder a la variable global
    if mode_switch.instate(["selected"]):  # Cuando esté en el estado "selected"
        style.theme_use("forest-light")
        bg_color = light_bg_color
        fg_color = light_fg_color
        current_theme = "light"  # Actualizar el tema actual
    else:
        style.theme_use("forest-dark")
        bg_color = dark_bg_color
        fg_color = dark_fg_color
        current_theme = "dark"  # Actualizar el tema actual

    root.configure(bg=bg_color)
    style.configure("TLabel", background=bg_color, foreground=fg_color)
    style.configure("TCheckbutton", background=bg_color, foreground=fg_color)

def enter_edit_mode():
    for button in all_buttons:
        button.grid_remove()
    for i, (combo, var) in enumerate(zip(all_combos, combo_vars)):
        combo.set(diccionario_botones[i + 1][1])
        combo.grid(row=i//3, column=i%3, padx=5, pady=5, sticky='news')
    accept_button.grid(row=4, column=1, padx=5, pady=(0,5), sticky="e")

def exit_edit_mode():
    accept_button.grid_remove()
    for combo in all_combos:
        combo.grid_remove()
    for button in all_buttons:
        button.grid()

def confirm_changes():
    changes = []
    for i, var in enumerate(combo_vars):
        if var.get() != diccionario_botones[i + 1][1]:
            changes.append(f"Botón {i + 1}: {diccionario_botones[i + 1][1]} -> {var.get()}")

    if changes:
        response = messagebox.askokcancel("Confirmar cambios", "\n".join(changes))
        if response:
            for i, var in enumerate(combo_vars):
                # Encuentra el nuevo archivo basado en la selección del texto
                nuevo_archivo = [k for k, v in procesos_disponibles.items() if v == var.get()][0]
                diccionario_botones[i + 1] = (nuevo_archivo, var.get())
                all_buttons[i].config(text=var.get(), command=lambda i=i: execute_command(i + 1))
            edit_switch.state(['!selected'])
            exit_edit_mode()
    else:
        edit_switch.state(['!selected'])
        exit_edit_mode()

root = tk.Tk()
root.focus_force()
root.title("Botonera Operativa")
root.resizable(False, False)


icono_path = get_resource_path(os.path.join(get_executable_directory(), "Assets/Icons", "botonera_icon.ico"))
root.iconbitmap(icono_path)

# -------------------
# Theme
# -------------------

style = ttk.Style(root)

theme_dir = os.path.join(get_executable_directory(), "Assets/Themes")
theme_files = ["forest-light.tcl", "forest-dark.tcl"]

for theme_file in theme_files:
    theme_path = os.path.join(theme_dir, theme_file)
    root.tk.call("source", theme_path)

# Define background and foreground (text) colors for each theme
light_bg_color = "#ffffff"  # Background color for light theme
dark_bg_color = "#313131"  # Background color for dark theme
light_fg_color = "#313131"  # Text color for light theme
dark_fg_color = "#eeeeee"  # Text color for dark theme

# Set initial theme and background color
style.theme_use("forest-dark")
current_theme = "dark"
root.configure(bg=dark_bg_color)

style.configure("TLabel", background=dark_bg_color, foreground=dark_fg_color)
style.configure("TCheckbutton", background=dark_bg_color, foreground=dark_fg_color)

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
# Frames
# -------------------

frame = ttk.Frame(root)
frame.pack(
    padx=10, pady=10, fill="both", expand=True
)

# -------------------
# Frames - Widgets
# -------------------

widgets_frame = ttk.LabelFrame(frame, text='Procesos disponibles')
widgets_frame.grid(row=0, column=0)

# Configurar el tamaño de las filas y columnas
widgets_frame.grid_rowconfigure(0, minsize=50)  # Establecer altura mínima de la fila 0
widgets_frame.grid_rowconfigure(2, minsize=50)  # Establecer altura mínima de la fila 0
widgets_frame.grid_columnconfigure(0, minsize=100)  # Establecer ancho mínimo de la columna 0
widgets_frame.grid_columnconfigure(1, minsize=100)  # Establecer ancho mínimo de la columna 0
widgets_frame.grid_columnconfigure(2, minsize=100)  # Establecer ancho mínimo de la columna 0

button_1 = ttk.Button(widgets_frame, text=diccionario_botones[1][1], command=lambda: execute_command(1))
button_1.grid(row=0, column=0, padx=5, pady=5, sticky='news')

button_2 = ttk.Button(widgets_frame, text=diccionario_botones[2][1], command=lambda: execute_command(2))
button_2.grid(row=0, column=1, padx=5, pady=5, sticky='news')

button_3 = ttk.Button(widgets_frame, text=diccionario_botones[3][1], command=lambda: execute_command(3))
button_3.grid(row=0, column=2, padx=5, pady=5, sticky='news')

button_4 = ttk.Button(widgets_frame, text=diccionario_botones[4][1], command=lambda: execute_command(4))
button_4.grid(row=2, column=0, padx=5, pady=5, sticky='news')

button_5 = ttk.Button(widgets_frame, text=diccionario_botones[5][1], command=lambda: execute_command(5))
button_5.grid(row=2, column=1, padx=5, pady=5, sticky='news')

button_6 = ttk.Button(widgets_frame, text=diccionario_botones[6][1], command=lambda: execute_command(6))
button_6.grid(row=2, column=2, padx=5, pady=5, sticky='news')

all_buttons = [button_1, button_2, button_3, button_4, button_5, button_6]

combo_vars = [tk.StringVar() for _ in range(6)]
all_combos = [ttk.Combobox(widgets_frame, textvariable=var, values=[v for v in procesos_disponibles.values()]) for var in combo_vars]

accept_button = ttk.Button(widgets_frame, text="Aceptar", command=confirm_changes)

edit_switch = ttk.Checkbutton(
    widgets_frame, text="Editar botones", style="Switch", command=enter_edit_mode
)
edit_switch.grid(row=4, column=0, padx=5, pady=(0,5), sticky="w")

mode_switch = ttk.Checkbutton(
    widgets_frame, text="Mode", style="Switch", command=toggle_mode
)
mode_switch.grid(row=4, column=2, padx=5, pady=(0,5), sticky="e")

root.mainloop()
