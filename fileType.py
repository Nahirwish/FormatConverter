from tkinter import Tk, filedialog
from tkinter import simpledialog
from tkinter import messagebox
import tempfile
import rarfile
import zipfile
import os

root = Tk()
root.withdraw()

def detectFormat(file):
    with open(file, 'rb') as f: # 'rb' (abrir el archivo en modo lectura y binario)
        head = f.read(8)
        if head.startswith(b'PK'):
            return 'zip'
        elif head.startswith(b'Rar!\x1A\x07\x00'):
            return 'rar (v4)'
        elif head.startswith(b'Rar!\x1A\x07\x01\x00'):
            return'rar (v5)'
        elif head.startswith(b'7z\xBC\xAF\x27\x1C'):
            return '7z'
        else:
            'unknown'


# Funciones para descomprimir
def processRar(file, dest_folder):
    print(' Entrando a process RAR ==============')
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            with rarfile.RarFile(file) as rf:
                rf.extractall(path=temp_dir)
        except rarfile.PasswordRequired:
            password = simpledialog.askstring(title='Contraseña requerida', prompt='Ingrese contraseña', show='*')
            if password:
                rf.extractall(path=temp_dir, pwd=password.encode())
            else:
                raise RuntimeError('No se ingreso contraseña')
        createCBZ(temp_dir, dest_folder)   
        
def processZip(file, dest_folder):
    print(' Entrando a process ZIP ==============')
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            with zipfile.ZipFile(file) as zf:
                zf.extractall(path=temp_dir)
        except RuntimeError:
            password = simpledialog.askstring(title='Contraseña requerida', prompt='Ingrese contraseña', show='*')
            if password:
                zf.extractall(path=temp_dir, pwd=password.encode('utf-8'))
            else:
                raise RuntimeError('No se ingreso contraseña')
        createCBZ(temp_dir, dest_folder) 

def createCBZ(temp_dir, destFolder):
    print('Ejecutando create CBR=============')
    with zipfile.ZipFile(destFolder, mode='w')as cbz:
        for folder, _, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(folder, file)
                relative_name = os.path.relpath(full_path, temp_dir)
                cbz.write(full_path, relative_name)
    messagebox.showinfo(' Se creó el CBZ correctamente')