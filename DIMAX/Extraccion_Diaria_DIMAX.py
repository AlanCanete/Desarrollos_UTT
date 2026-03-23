import datetime
import shutil

def obtienefecha():
    today = datetime.date.today()
    dia = today.day
    mes = today.month
    agno = today.year
    if dia < 10:
        dia = f"0{dia}"
    if mes < 10:
        mes = f"0{mes}"
    return dia, mes, agno

def obtieneArchivo(file):
    hostname='//sftp-2'
    username = 'Administrador'
    password = 'Upthetrade2016'

    remotepath=f'{hostname}/D/DIMAK/HISTORIA/{file}.csv'
    localpath=f'//produccion19/Dimak/{file}.csv'

    try:
        shutil.copy(remotepath,localpath)
    except Exception as e:
        print(f"Ocurrio un error: {e}")

dia, mes, agno = obtienefecha()
print(dia,mes,agno)

obtieneArchivo(f"LOCALES_{agno}{mes}{dia}")
obtieneArchivo(f"VENTAS_{agno}{mes}{dia}")
obtieneArchivo(f"PRODUCTOS_{agno}{mes}{dia}")