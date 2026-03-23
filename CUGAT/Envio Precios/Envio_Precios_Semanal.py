import subprocess
import datetime
import sys
import pyodbc
from pathlib import Path

ruta = '//produccion5/D/CUGAT/'
file = 'PRECIOS_CUGAT_'

def obtieneSemana():
    today = datetime.date.today()
    agno_iso, semana_iso, dia_semana_iso = today.isocalendar()
    semanaCalendar = semana_iso
    agnoCalendar = agno_iso
    
    if semanaCalendar == 1:
        semanaCalendar = 52
    else:
        semanaCalendar = semanaCalendar - 1 

    return semanaCalendar

def crearRar(ruta_entrada, salida_rar, nivel_compresion=5,sobreescribir =True):
    ruta_entrada = Path(ruta_entrada).expanduser().resolve()
    salida_rar = Path(salida_rar).expanduser().resolve()

    if not salida_rar.suffix.lower() == ".rar":
        salida_rar = salida_rar.with_suffix(".rar")
    
    if not ruta_entrada.exists():
        raise FileNotFoundError(f"No se encontro la ruta de entrada: {ruta_entrada}")

    rar_cmd = None
    if sys.platform.startswith("win"):
        posibles = [
            r"C:\Program Files\WinRAR\Rar.exe",
            r"C:\Program files (x86)\WinRar\Rar.exe"
        ]
        for p in posibles:
            if Path(p).exists():
                rar_cmd = p
                break

    if rar_cmd is None:
        rar_cmd="rar"

    try:
        nivel_compresion = max(0, min(5, int(nivel_compresion)))
    except Exception:
        nivel_compresion = 5

    args = [rar_cmd,"a", f"-m{nivel_compresion}","-r","-ep1"]
    if ruta_entrada.is_dir():
        args.append("-r")
    if sobreescribir:
        args.append("-o+")
    args.append(str(salida_rar))    
    
    if ruta_entrada.is_dir():
        input_spec = "*"
        cwd = str(ruta_entrada)
        args.append(input_spec)
    else:
        cwd=None
        args.append(str(ruta_entrada))

    print("Ejecuntado:"," ".join(args))    
    try:
        completed = subprocess.run(
            args=args,
            check=True,
            cwd=cwd,
            shell=sys.platform.startswith("win"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        print(completed.stdout)
        return str(salida_rar)
    except subprocess.CalledProcessError as e:
        print("STDOUT:\n", e.stdout)
        print("STDERR:\n", e.stderr)
        raise RuntimeError(
            f"WinRar fallo con codigo {e.returncode}. "
            f"Revisa las rutas y opciones. Mensaje:\n{e.stderr or e.stdout}"
        )

def envioMailAdjunto(archivoRar,semana):
    servermail = 'PRODUCCION8'
    databaseemail = 'DQC'
    useremail = 'acanete'
    passemail = 'Canete2025@utt'
    conec_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={servermail};DATABASE={databaseemail};UID={useremail};PWD={passemail}'
    destinatario= 'egonzalez@cugat.cl;emege@cugat.cl;mgalaz@cugat.cl;rtoro@cugat.cl'
    copiaemail = 'jhonathan.alvarez@upthetrade.com;karelys.caraballo@utt.cl;carlos.matus@upthetrade.com;joseluis.romero@utt.cl;alan.canete@upthetrade.com'
    asunto=f'Precios Cugat semana {semana}'

    try:
        conn = pyodbc.connect(conec_string)
        cursor = conn.cursor()
        procedure = 'sp_EjecutaMail_CUGAT_PRECIOS'
        parametros = (destinatario,copiaemail,asunto,archivoRar)
        call_procedure = f"EXEC {procedure} ?,?,?,?"
        cursor.execute(call_procedure, parametros)
        conn.commit()
    except Exception as ex:
        print(f"Ocurrio un error: {ex}")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        if sqlstate == '28000':
            print("Error de autenticacion")
        else:
            print(f"Error al ejecutar el procedure: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

try:
    semana = obtieneSemana()
    print(semana)
    fileori = f'{ruta}{file}{semana}.csv'
    filerar = f'{ruta}{file}{semana}.rar'
    
    crearRar(fileori,filerar,nivel_compresion=5)
    envioMailAdjunto(filerar,semana)
except Exception as ex:
    print(ex)

