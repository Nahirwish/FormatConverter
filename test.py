import os
import sys
import shutil
import tempfile
import zipfile
from tkinter import Tk, filedialog
from tkinter import messagebox
from tkinter import simpledialog
import rarfile
# Primer intento, no captura bien las excepciones

root = Tk()
root.withdraw()

ruta_cbr = filedialog.askopenfilename(title='Seleccionar archivo', filetypes=[('Archivos CBR o RAR', '*.rar')]) # Ruta del rar

if not ruta_cbr:
    print('No se selecciono archivo')
    exit()


ruta_destino = filedialog.asksaveasfilename(title=' Guardar como cbz', defaultextension='.cbz', filetypes=[('Comic book ZIP', '*.cbz')])

# Crear carpeta temporal pra las imagenes
with tempfile.TemporaryDirectory() as temp_dir:
    try:
        extraido = False
        # Probar con rar
        try:
            with rarfile.RarFile(ruta_cbr) as rf:
                rf.extractall(path=temp_dir)
                print(' Archivo extraido como rar')
        except rarfile.PasswordRequired:
            password = simpledialog.askstring("Contraseña requerida")
            if password:
                with rarfile.RarFile(ruta_cbr) as rf:
                    rf.extractall(path= temp_dir, pwd=password)
                    print(' Rar EXTraido con contraseña')
                    extraido = True
            else:
                raise RuntimeError("No se ingreso contraseña rar")
        
        except rarfile.NeedFirstVolume:
            messagebox.showerror("Error", "Este archivo RAR es parte de un conjunto dividido.")
            exit()   
        
        except rarfile.BadRarFile:
            try:
            # Intentar abrir como zip        
                with zipfile.ZipFile(ruta_cbr) as zf:
                    try:
                        zf.extractall(path=temp_dir)
                        print(' Archivo extraido como zip sin contraseña')
                    except RuntimeError:
                        password = simpledialog.askstring("Contraseña requerida")
                        if password:
                            zf.extractall(temp_dir, pwd=password.encode('utf-8'))
                            extraido = True
                            print(" Archivo extraido CON contraseña")
                        else:
                            raise RuntimeError("No se ingreso contraseña")
            except zipfile.BadZipFile:
                raise RuntimeError("No es un ZIP válido")            
            
        if not extraido:
            raise RuntimeError("nO SE PUEDE EXTRAER EL ARCHIVO")
        
        
        # Crear archivo cbz ======================================
        with zipfile.ZipFile(ruta_destino, mode='w', compression=zipfile.ZIP_DEFLATED) as cbz:
            for foldername, subfolders, filenames in os.walk(temp_dir):
                for filename in filenames:
                    full_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(full_path, temp_dir)
                    cbz.write(full_path, arcname)
                    print(f'{arcname} Añadido al cbz')
        print(' Conversion completada')
    except Exception as e:
        messagebox.showerror( "Error durante la conversion", e)