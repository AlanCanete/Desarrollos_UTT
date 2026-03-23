import pyodbc
import csv
import datetime

Server = 'clientes1'
database = 'CLIENTES'
user = 'acanete'
password = 'Canete2025@utt'
conection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={Server};DATABASE={database};UID={user};PWD={password}'
destino = '//produccion20/XLSX/ARIZTIA/SEMANAL/Planos/'
nameFile = 'POLLOSPAVOS_ARIZTIA'

def ObtieneAgnoSemana():
    today = datetime.date.today()
    agno_iso, semana_iso, dia_iso = today.isocalendar()
    if semana_iso == 1:
        agno = agno_iso - 1
        semana = 12
    else:
        agno = agno_iso
        semana = semana_iso - 1

    return agno,semana

try:
    agno_f, semana_f = ObtieneAgnoSemana()
    aux = str(agno_f)
    agnoCut = aux[2:4]
    conn = pyodbc.connect(conection_string)
    cursor = conn.cursor()

    query = "SELECT * FROM [CLIENTES].[dbo].[POLLOAPAVOS_KEYACCOUNT_ARIZTIA_TXT] WITH(NOLOCK)"

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]

    with open(f"{destino}{nameFile}.csv",'w',newline='',encoding='utf-8')as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(columns)
        for row in cursor.fetchall():
            writer.writerow(row)
    
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error al conectar a SQL Server: {sqlstate}")
    exit()
except Exception as e:
    print(f"Ocurrio un error: {e}")
finally:
    cursor.close()
    conn.close()