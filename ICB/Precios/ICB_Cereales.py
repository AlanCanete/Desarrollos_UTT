import pyodbc
import csv

Server = 'DEV01'
database = 'DEV'
user = 'acanete'
password = 'Canete2025@utt'
conection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={Server};DATABASE={database};UID={user};PWD={password}'
destino = '//produccion20/XLSX/ICB/'
nameFile = 'ICB_Cereales.csv'

try:
    conn = pyodbc.connect(conection_string)
    cursor = conn.cursor()
    query = "SELECT * FROM tblCereales_txt With(Nolock)"

    #print(query)

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    with open(destino+nameFile,'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(columns)
        for row in cursor.fetchall():
            writer.writerow(row)
    cursor.close()
    conn.close()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error al conectar a SQL Server: {sqlstate}")
    exit()
except Exception as e:
    print(e)