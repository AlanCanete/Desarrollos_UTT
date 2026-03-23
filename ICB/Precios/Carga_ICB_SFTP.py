import shutil
import os


def CopyFile(nomFile):
    rutaFileICB = '//192.168.2.77/ICB/PRECIOS/'
    rutaLocal = f'//produccion20/XLSX/ICB/{nomFile}'

    if os.path.exists(rutaLocal):
        shutil.copy(rutaLocal, rutaFileICB)
        print(f"Archivo copaido de {rutaLocal} a {rutaFileICB}")
    else:
        print(F"El archivo de origen no existe: {rutaLocal}")

CopyFile('ICB_SaborizantesLeche.csv')
CopyFile('ICB_Cereales.csv')
CopyFile('ICB_ConservasFutrasVerduras.csv')
#CopyFile('ICB_MultiSnacks.csv')
CopyFile('ICB_Te.csv')