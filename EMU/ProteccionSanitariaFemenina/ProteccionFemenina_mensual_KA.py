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
nameFile = 'PROTECCION_SANITARIA_FEMENINA_MENSUAL_'

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

    query = "SELECT [agno],[mes],[empresa],[cadena],[upc],[descri_item],[fabricante],[marca],[categoria],[submarca],[longitud],[espesor],[cubierta],[alas],[promocion],[codigo]"
    query = query + ",[tier],[aplicador],[conteo],[tipo],[con_perfume_sin_perfume],[peso],[unidades],[gramaje],[region_utt],[ciudades_utt],[canal],[tipo_retail],[segmento],[tier_conteo]"
    query = query + ",sum([ventauni]) as vta_uni,sum([ventapesos]) as vta_pesos,sum([ventaconvertida]) as vta_convertida FROM [CLIENTES].[dbo].[PSF_KEYACCOUNT_FARMACIAS_SUPERMERCADOS_EMU] WITH(NOLOCK)"
    query = query + "WHERE agno >=2021 GROUP BY agno,mes,empresa,cadena,upc,descri_item,fabricante,marca,categoria,submarca,longitud,espesor,cubierta,alas,promocion,codigo,tier,aplicador,conteo,"
    query = query + "tipo, con_perfume_sin_perfume, peso,unidades,gramaje,region_utt,ciudades_utt, canal,tipo_retail,segmento,tier_conteo"

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    with open(f"{destino}{nameFile}{agno_f}_{mes_f}.csv",'w',newline='', encoding='utf-8')as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(columns)
        for row in cursor.fetchall():
            new_row = []
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
