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
archivoCSV ="MANTEQUILLAMARGARINA_Mensual"

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
    query = "SELECT [agno] AS AÑO ,[mes] AS MES,[nmes] AS NMES,[fecha] AS FECHA,[pan_uam] AS PAM_UAM,[Periodo_YTD],[upc] AS UPC,[descri_item] AS DESCRI_ITEM ,[categoria_colun] AS CATEGORIA"
    query = query + ",[subcategoria_colun] AS SUBCATEGORIA,[natural_sabor_colun] AS NATURAL_SABOR,[fabricante_colun] AS FABRICANTE,[marca_colun] AS MARCA,[regular_light_colun] AS REGULAR_LIGHT"
    query = query + ",[con_sin_lactosa_colun] AS CON_SIN_LACTOSA,[envase_colun] AS ENVASE,[tamano_colun] AS TAMAÑO,[procedencia_colun] AS PROCEDENCIA,[zona_colun] AS ZONA,[zona_nacional_colun] AS ZONA_NACIONAL"
    query = query + ",[microzona_colun] AS MICROZONA, [atributo_colun] AS ATRIBUTO,[segmento_colun] AS SEGMENTO,[cadena] AS CADENA,[canal],SUM ([ventauni]) AS VENTA_UNIDADES,SUM ([ventapesos]) AS VENTA_PESOS"
    query = query + ",SUM ([ventapesos_miles]) AS VENTA_PESOS_MILES,SUM ([ventaconvertida]) AS VENTA_CONVERTIDA,SUM ([ventaconvertida_miles]) AS VENTA_CONVERTIDA_MILES FROM [CLIENTES].[dbo].[MANTEQUILLA_MARGARINA_KEYACCOUNT_COLUN] "
    query = query + "where agno > '2021' group by [agno],[mes],[nmes],[fecha],[pan_uam],[Periodo_YTD],[upc],[descri_item],[categoria_colun],[subcategoria_colun],[natural_sabor_colun],[fabricante_colun],[marca_colun]"
    query = query + ",[regular_light_colun],[con_sin_lactosa_colun],[envase_colun],[tamano_colun],[procedencia_colun],[atributo_colun],[segmento_colun],[zona_colun],[zona_nacional_colun],[microzona_colun],[cadena],[canal]"
    
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