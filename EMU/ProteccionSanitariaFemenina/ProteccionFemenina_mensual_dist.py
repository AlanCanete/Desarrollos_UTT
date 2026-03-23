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
nameFile = 'PROTECCION_SANITARIA_FEMENINA_MENSUAL_DIST_'

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

    query = "SELECT  [agno],[mes],[upc],[descri_item],[categoria],[fabricante],[marca],[submarca],[longitud],[alas],[codigo],[tier],[unidades],[con_perfume_sin_perfume],[aplicador]"
    query = query + ",[segmento],[peso],[gramaje],[tier_conteo],[canal],[tipo_retail],[promocion],[tipo],[conteo],[cubierta],[espesor],[empresa],[cadena],[ciudades_utt],[localtrabajando]"
    query = query + ",[universo],[ventauniverso],[ventalocales] FROM [CLIENTES].[dbo].[PSF_KEYACCOUNT_FARMACIAS_SUPERMERCADOS_EMU_DISTRIBUCION] WITH(NOLOCK)"
    
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
