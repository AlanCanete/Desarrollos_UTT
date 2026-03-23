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
nameFile = 'TOALLAS_HUMEDAS_MENSUAL_'

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

    query = "select [agno],[mes],[upc],[descri_item],[empresa],[categoria],[fabricante],[marca],[tipo],[tipo_2] as infantil_adulto,[envase]"
    query = query +",[presentacion],[unidades],[peso],[gramaje],[cadena],[region_utt],[ciudades_utt],[canal],[tipo_retail],[tamano_emu]"
    query = query +",[tipo_emu],cast(sum([ventauni]) as Int) as vta_uni,cast(sum([ventapesos])as numeric(18,0)) as vta_pesos ,cast(sum([ventaconvertida]) as numeric(18,0)) as vta_convertida "
    query = query + "FROM [CLIENTES].[dbo].[TOALLAS_HUMEDAS_KEYACCOUNT_MENSUAL_EMU] WITH(NOLOCK) WHERE [agno] >=2021 GROUP BY agno,mes,upc,"
    query = query + "descri_item,empresa,categoria,fabricante,marca,tipo,tipo_2,envase,presentacion,unidades,peso,gramaje,cadena,region_utt,"
    query = query + "ciudades_utt,canal,tipo_retail,tamano_emu,tipo_emu"

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    with open(f"{destino}{nameFile}{agno_f}_{mes_f}.csv",'w',newline='', encoding='utf-8')as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(columns)
        for row in cursor.fetchall():
            new_row=[]
            for val in row:
                if isinstance(val, float):
                    new_row.append(str(val).replace('.',','))
                else:
                    new_row.append(val)
            writer.writerow(row)
    cursor.close()
    conn.close()
except pyodbc.Error as ex:
    sqlstate = ex.args[1]
    print(f"Error al conectar a SQL Server: {sqlstate}")
    exit()
except Exception as e:
    print(e)
