import os
import sys
import shutil
import tempfile
import zipfile
from tkinter import Tk, filedialog
from tkinter import messagebox
from tkinter import simpledialog
import rarfile

import fileType as ft


root = Tk()
root.withdraw()

# Seleccionar archivo y detectar formato
file = filedialog.askopenfilename(title="Seleccionar archivo para convertir", filetypes=[('Archivo CBR o RAR','*.rar' )])
format = ft.detectFormat(file)
dest_folder = filedialog.asksaveasfilename(title='Guardar como cbz', defaultextension='.cbz', filetypes=[('Comic book ZIP', '*.cbz')])

# Llamar a la funcion segun el formato 
if format == '7z' or format == 'unknown':
    messagebox.showerror(title='Formato no soportado', message= f'No es posible descomprimir la extensión{format}')
    exit()
elif format == 'rar (v4)' or format == 'rar (v5)':
    print(' Archivo rar: llamando a la funcion . . .')
    ft.processRar(file, dest_folder)
elif format == 'zip':
    print(' Archivo zip: llamando a la funcion . . .')
    ft.processZip(file, dest_folder)

