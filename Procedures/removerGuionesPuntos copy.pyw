#------------------------------------
# CÓDIGO
#------------------------------------
"""Este es un código para modificar masivamente los nombre de archivos.
Este código busca los archivos en la carpeta en que se ejecuta que tengan "- " y que no sean .py o .pyw
A los archivos que cumplan esas condiciones, los renombra sacando "- "
Los archivos renombrados se guardan en una nueva carpeta llamada "Archivos renombrados"
"""


import os  # noqa: E402
import shutil  # noqa: E402
from tkinter import Tk, messagebox, filedialog  # noqa: E402
import sys  # noqa: E402


# Función para mostrar un mensaje en un cuadro de diálogo
def mostrar_mensaje(mensaje):
    messagebox.showinfo("Información", mensaje)

def get_executable_directory():
    # Obtiene la ubicación del directorio donde se encuentra el ejecutable
    if getattr(sys, 'frozen', False):
        # Modo ejecutable (compilado)
        return os.path.dirname(sys.executable)
    else:
        # Modo script (desarrollo)
        return os.path.dirname(os.path.abspath(__file__))


# Crear una instancia de Tkinter y ocultar la ventana principal
root = Tk()
root.withdraw()


# Establecer el icono personalizado

icon_dir = os.path.join(get_executable_directory(), "Assets/Icons")
icon_file = "botonera_icon.ico"

icono_path = os.path.join(icon_dir, icon_file)
root.iconbitmap(icono_path)


# Mostrar un cuadro de diálogo para seleccionar una carpeta
directorio_actual = filedialog.askdirectory(title="Selecciona una carpeta")

# Verificar si se ha seleccionado una carpeta
if not directorio_actual:
    mostrar_mensaje("No se ha seleccionado ninguna carpeta.")
else:
    # Listar todos los archivos en el directorio seleccionado
    archivos = os.listdir(directorio_actual)
    archivos_renombrados = 0

    for archivo in archivos:
        # Obtener la extensión del archivo
        nombre_base, extension = os.path.splitext(archivo)
        # print(nombre_base)
        # print(extension)

        # Excluir archivos con extensión .py y .pyw
        if extension not in ['.py', '.pyw']:
            # Comprobar si "- " está en cualquier lugar del nombre del archivo
            # if "- " in archivo or "-" in archivo or "." in archivo:
            if "- " in archivo or "-" in archivo or "." in archivo:
                # Crear el nuevo nombre del archivo sin "- " y sin puntos en la raíz del nombre
                nuevo_nombre = nombre_base.replace("- ", "").replace(".", "").replace("-", "") + extension

                # Rutas completas al archivo original y al nuevo archivo
                ruta_vieja = os.path.join(directorio_actual, archivo)
                ruta_nueva = os.path.join(directorio_actual, nuevo_nombre)

                # Copiar el archivo
                shutil.copy2(ruta_vieja, ruta_nueva)

                # Eliminar el archivo original
                os.remove(ruta_vieja)
                
                # Contabilizar archivo copiado y renombrado
                archivos_renombrados += 1

    # Mostrar mensaje con la cantidad de archivos copiados y renombrados
    mensaje_final = f'Se han renombrado {archivos_renombrados} archivos.'
    mostrar_mensaje(mensaje_final)

