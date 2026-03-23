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
archivoCSV ="CREMASLECHE_Mensual"

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
    query = "SELECT [agno] AS AGNO,[mes] AS MES,[nmes] AS NMES,[fecha] AS FECHA,[pan_uam] AS PAM_UAM,[Periodo_YTD],[upc] AS UPC,[descri_item] AS DESCRI_ITEM,[categoria] AS CATEGORIA"
    query = query + ",[segmento_colun] AS SUBCATEGORIA,[subsegmento_colun] AS SUBSEGMENTO,[atributo_colun] AS ATRIBUTO,[blanca_sabor] AS BLANCA_SABOR,[sabor_colun] AS SABOR"
    query = query + ",[con_sin_azucar_colun] AS CON_SIN_AZUCAR,[fabricante_colun] AS FABRICANTE,[marca_colun] AS MARCA,[con_sin_lactosa_colun] AS SEGMENTO,[regular_light_colun] AS REGULAR_LIGHT"
    query = query + ",[envase_colun] AS ENVASE,[presentacion_colun] AS PRESENTACION,[tamano_colun] AS TAMAÑO,[tamano_unificado_colun] AS TAMAÑO_UNIFICADO,[zona_colun] AS ZONA"
    query = query + ",[zona_nacional_colun] AS ZONA_NACIONAL,[microzona_colun] AS MICROZONA,[cadena] AS CADENA,[canal],SUM ([ventauni]) AS VENTA_UNIDADES,SUM ([ventapesos]) AS VENTA_PESOS"
    query = query + ",SUM ([ventapesos_miles]) AS VENTA_PESOS_MILES,SUM ([ventaconvertida]) AS VENTA_CONVERTIDA,SUM ([ventaconvertida_miles]) AS VENTA_CONVERTIDA_MILES"
    query = query + " FROM [CLIENTES].[dbo].[CREMAS_LECHE_KEYACCOUNT_COLUN] WHERE AGNO > '2021' GROUP BY [agno],[mes],[nmes],[fecha],[pan_uam],[Periodo_YTD],[upc],[descri_item],[categoria]"
    query = query + ",[segmento_colun],[subsegmento_colun],[atributo_colun],[blanca_sabor],[sabor_colun],[con_sin_azucar_colun],[fabricante_colun],[marca_colun],[con_sin_lactosa_colun]"
    query = query + ",[regular_light_colun],[envase_colun],[presentacion_colun],[tamano_colun],[tamano_unificado_colun],[zona_colun],[zona_nacional_colun],[microzona_colun],[cadena],[canal]"

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