import pyodbc
import csv
import shutil
import datetime

server = 'CLIENTES3'
database = 'CLIENTES'
username = 'acanete'
password = 'Canete2025@utt'
conection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
destino = '//produccion20/XLSX/EMU/CSV/'
#destino = 'C:/Users/Alan Cañete/Desktop/Analisis xlsx/'
nameFile = 'INCONTINENCIA_MENSUAL_DIST_'

def ObtieneSemana():
    today = datetime.datetime.now()
    agno = today.year
    mes = today.month

    if mes == 1:
        agno_file = agno -1
        mes_file = 12
    else:
        agno_file = agno
        mes_file = mes -1 
    return agno_file, mes_file


try:
    agno_f, mes_f = ObtieneSemana()
    conn = pyodbc.connect(conection_string)
    cursor = conn.cursor()

    query = "  SELECT [agno],[mes],[upc],[descri_item],[categoria],[fabricante_essity] as fabricante,[marca_essity] as marca,[submarca_essity] as submarca,[segmento_etario]"
    query = query + ",[segmento],[subsegmento_essity] as subsegmento,[segmento_agrupado_essity] as segmento_agrupado,[talla],[presentacion_regular],[promocion_nopromocion]"
    query = query + ",[empaque_envase],[contenido_en_unidades],[conteo_essity] as conteo,[empresa],[tipo_retail],[cadena],[ciudades_utt],[localtrabajando],[universo]"
    query = query + ",cast([ventauniverso] as float) as ventauniverso,cast([ventalocales] as float) as ventalocales FROM [CLIENTES].[dbo].[INCONTINENCIA_KEYACCOUNT_MENSUAL_DISTRIBUCION] WITH(NOLOCK) WHERE [agno] >= 2021"

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    with open(f"{destino}{nameFile}{agno_f}_{mes_f}.csv",'w',newline='', encoding='utf-8')as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(columns)
        for row in cursor.fetchall():
            new_row =[]
            for val in row:
                if isinstance(val, float):
                    new_row.append(str(val).replace('.',','))
                else:
                    new_row.append(val)
            writer.writerow(row)
    cursor.close()
    conn.close()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error al conectar a SQL Server: {sqlstate}")
    exit()
except Exception as e:
    print(e)
