import pyodbc
import csv
import pandas as pd
import datetime

server = 'DEV01'
database = 'DEV'
username = 'acanete'
password = 'Canete2025@utt'
coneionString = f'DRIVER={{ODBC Driver 17 for SQL Server}}; SERVER={server};DATABASE={database};UID={username};PWD={password}'
rutatxt = "//PRODUCCION20/XLSX/BALLERINA/TXT/"
#rutatxt = "C:/Users/Alan Cañete/Desktop/desarrollos_datos/"
filetxt ="FILTROS_SOLARES_SL_M"

def obtieneSemana():
    today = datetime.date.today()
    agno_iso, semana_iso, dia_semana_iso = today.isocalendar()
    semanaCalendar = semana_iso -1
    agnoCalendar = agno_iso
    return semanaCalendar, agnoCalendar

try:
    sp_name = "exec sp_ObtienePlanosFiltrosSolares"
    conn = pyodbc.connect(coneionString)
    cursor = conn.cursor()
    cursor.execute(sp_name)
    columns = [column[0] for column in cursor.description]

    with open(f"{rutatxt}{filetxt}.txt",'w', newline='', encoding='utf-8') as txtfile:
        writer = csv.writer(txtfile, delimiter=';')
        writer.writerow(columns)
        for row in cursor.fetchall():
            writer.writerow(row)


except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error al conectar a SQL Server: {sqlstate}")
    exit()
except Exception as e:
    print(e)
finally:
    cursor.close()
    conn.close()