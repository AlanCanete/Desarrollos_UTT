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
archivoCSV ="QUESOS_Mensual"

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
    query = "SELECT [agno] AS AÑO,[mes] AS MES,[nmes] AS NMES,[fecha] AS FECHA,[pan_uam] AS PAM_UAM,[Periodo_YTD],[upc] AS UPC,[descri_item] AS DESCRI_ITEM,[categoria] AS CATEGORIA,[subcat_colun] AS SUBCATEGORIA"
    query = query + ",[segmento_colun] AS SEGMENTO,[tipo_colun] AS TIPO,[envasado_granel_colun] AS ENVASADO,[fabricante_colun] AS FABRICANTE,[marca_colun] AS MARCA,[light_no_light_colun] AS REGULAR_LIGHT,[con_sin_lactosa_colun] AS CON_SIN_LACTOSA"
    query = query + ",[natural_sabor_colun] AS NATURAL_SABOR,[empaque_colun] AS EMPAQUE,[formato_colun] AS FORMATO,[tamano_colun] AS TAMAÑO,[jerarquia_colun] AS JERARQUIA,[presentacion_colun] AS PRESENTACION,[alta_baja_humedad] AS ALTA_BAJA_HUMEDAD"
    query = query + ",[lamina_normal_gruesa] AS LAMINA_NORMAL_GRUESA, [maduracion_colun] as maduracion,[zona_colun] AS ZONA,[zona_nacional_colun] AS ZONA_NACIONAL,[microzona_colun] AS MRICOZONA,[cadena] AS CADENA"
    query = query + ",[canal],sum ([ventauni]) as Venta_Unidades,sum ([ventapesos]) as Venta_Pesos,sum ([ventapesos_miles]) as Venta_Pesos_Miles,sum ([ventaconvertida]) as Venta_Convertida,sum ([ventaconvertida_miles]) as Venta_Convertida_Miles "
    query = query + "FROM [CLIENTES].[dbo].[QUESOS_KEYACCOUNT_COLUN] with (nolock) Where agno > '2022' Group by [agno],[mes],[nmes],[fecha],[pan_uam],[Periodo_YTD],[upc],[descri_item],[categoria],[subcat_colun],[segmento_colun]"
    query = query + ",[tipo_colun],[envasado_granel_colun],[fabricante_colun],[marca_colun],[light_no_light_colun],[con_sin_lactosa_colun],[natural_sabor_colun],[empaque_colun],[formato_colun],[tamano_colun],[jerarquia_colun], [presentacion_colun]"
    query = query + ",[alta_baja_humedad],[lamina_normal_gruesa],[maduracion_colun],[zona_colun],[zona_nacional_colun],[microzona_colun],[cadena],[canal]"
    
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