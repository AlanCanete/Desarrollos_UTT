import pyodbc
import csv
import pandas as pd
import datetime

server = 'Clientes2'
database = 'CLIENTES'
username = 'acanete'
password = 'Canete2025@utt'
coneionString = f'DRIVER={{ODBC Driver 17 for SQL Server}}; SERVER={server};DATABASE={database};UID={username};PWD={password}'
rutaCSV = "//PRODUCCION20/XLSX/COLUN/INTERFACES/MENSUAL/"
archivoCSV ="CANASTALACTEA_Mensual"

def armaFecha():
    today = datetime.datetime.today()
    ini_week = datetime.timedelta(days=10)
    end_week = datetime.timedelta(days=4)
    lunes_past = today - ini_week
    domingo_past = today - end_week

    if lunes_past.month < 10:
        mes = f'0{lunes_past.month}'
    else:
        mes = lunes_past.month

    if lunes_past.day < 10:
        dia = f'0{lunes_past.day}'
    else:
        dia = lunes_past.day

    if domingo_past.month <10:
        mes2 = f'0{domingo_past.month}'
    else:
        mes2 = domingo_past.month

    if domingo_past.day < 10:
        dia2 = f'0{domingo_past.day}'
    else:
        dia2 = domingo_past.day

    fechaNombre = f'({dia}-{mes} al {dia2}-{mes2})'
    return fechaNombre


try:
    conn = pyodbc.connect(coneionString)
    cursor = conn.cursor()
    query = "SELECT [AGNO],[NMES],[CATEGORIA],[FABRICANTE],[SEGMENTO],[ZONA NACIONAL],[MICROZONA],[CADENA],[CANAL],sum([VENTA_UNIDADES]) as ventauni,sum([VENTA_PESOS]) as ventapesos,sum([VENTA_PESOS_MILES]) as ventapesos_miles"
    query = query + ",sum([VENTA_CONVERTIDA]) as ventaconvertida,sum([VENTA_CONVERTIDA_MILES]) as ventaconvertida_miles FROM [CLIENTES].[dbo].[MULTICATEGORIA_COLUN] where AGNO >= 2023 Group by [AGNO] ,[NMES] ,[CATEGORIA] ,[FABRICANTE]"
    query = query + ",[SEGMENTO],[ZONA NACIONAL],[MICROZONA],[CADENA],[CANAL]"
    #print(query)
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    with open(rutaCSV+archivoCSV+'.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer =csv.writer(csvfile, delimiter=",")
        writer.writerow(columns)
        for row in cursor.fetchall():
            writer.writerow(row)
    cursor.close()
    conn.close

except pyodbc.Error as ex:
    sqlstate = ex.args[1]
    print(f"Error al conectar a SQL Server: {sqlstate}")
    exit()
except Exception as e:
    print(e)