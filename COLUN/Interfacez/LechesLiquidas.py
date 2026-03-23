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
archivoCSV ="LECHESLIQUIDAS_Mensual"

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
    query = "SELECT [agno] AS AÑO,[mes] AS MES,[nmes] AS NMES,[fecha] AS FECHA,[pan_uam] AS PAM_UAM,[upc] AS UPC,[descri_item] AS DESCRI_ITEM,[categoria] AS CATEGORIA,[subcategoria_colun] AS SUBCATEGORIA"
    query = query + ",[blanca_sabor_colun] AS BLANCA_SABOR,[materia_grasa_colun] AS MATERIA_GRASA,[fabricante_colun] AS FABRICANTE,[marca_colun] AS MARCA ,[regular_light_colun] AS REGULAR_LIGHT,[con_sin_lactosa_colun] AS segmento"
    query = query + ",[envase_colun] AS ENVASE,[tamano_colun] AS TAMAÑO,[tamano_unificado_colun] AS TAMAÑO_UNIFICADO,[agrup_tamano_colun] AS AGRUP_TAMAÑO ,[presentacion_colun] AS PRESENTACION ,[sabor_colun] AS SABOR"
    query = query + ",[jerarquia_colun] AS JERARQUIA,[zona_colun] AS ZONA,[zona_nacional_colun] AS ZONA_NACIONAL,[microzona_colun] AS MICROZONA, [leche_larga_vida_fresca] AS LARGAVIDA_FRESCA, [con_sin_proteinas] AS ATRIBUTO"
    query = query + ",[bebida_lactea_leche] AS BEBIDA_LACTEA ,[cadena] AS CADENA,[canal],[Periodo_YTD],sum ([ventauni]) AS VENTA_UNIDADES,SUM ([ventapesos]) AS VENTA_PESOS,SUM ([ventapesos_miles]) AS VENTA_PESOS_MILES"
    query = query + ",SUM ([ventaconvertida]) AS VENTA_CONVERTIDA,SUM ([ventaconvertida_miles]) AS VENTA_CONVERTIDA_MILES FROM [CLIENTES].[dbo].[LECHES_LIQUIDAS_KEYACCOUNT_COLUN] WHERE AGNO > '2021' GROUP BY [agno]"
    query = query + ",[mes],[nmes],[fecha],[pan_uam],[upc],[descri_item],[categoria],[subcategoria_colun],[blanca_sabor_colun],[materia_grasa_colun],[fabricante_colun],[marca_colun],[regular_light_colun],[con_sin_lactosa_colun]"
    query = query + ",[envase_colun],[tamano_colun],[tamano_unificado_colun],[agrup_tamano_colun],[presentacion_colun],[sabor_colun],[jerarquia_colun],[zona_colun],[zona_nacional_colun],[microzona_colun], [leche_larga_vida_fresca]"
    query = query + ",[con_sin_proteinas],[bebida_lactea_leche],[cadena],[canal],[Periodo_YTD],[region_utt]"
    
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