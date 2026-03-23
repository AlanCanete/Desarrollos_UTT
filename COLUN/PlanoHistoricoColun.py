import pyodbc
import csv
import datetime

def ultimasemana():
    today = datetime.date.today()
    agno = today.year
    numero_semana_actual = today.isocalendar()[1]
    lunes_ant = today - datetime.timedelta(days=today.weekday()+7)
    domingo_ant =  lunes_ant + datetime.timedelta(days=6)#today - datetime.timedelta(days=today.weekday()+1)

    if numero_semana_actual == 1:
        semanaTrabajo = 52
        agnotrabajo = int(agno) - 1
    else:
        semanaTrabajo = numero_semana_actual - 1
        agnotrabajo = int(agno)

    return lunes_ant,domingo_ant,f"{semanaTrabajo:02}", agnotrabajo

Server = 'DEV01'
database = 'DEV'
user = 'acanete'
password = 'Canete2025@utt'
conection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={Server};DATABASE={database};UID={user};PWD={password}'
destino = '//produccion20/XLSX/COLUN/INTERFACES/PRECIOS/'
nameFile = 'HISTORICOS_PRECIOS_COLUN_2025'

try:
    lunes,domingo,semana,agno = ultimasemana()
    desde=20251229
    hasta=20260104
    conn = pyodbc.connect(conection_string)
    cursor = conn.cursor()
    query = "SELECT DimFechaColun.ID_Fecha, DimProductoColun.UPC, DimFechaColun.Fecha, DimFechaColun.Agno, DimFechaColun.Mes, DimFechaColun.semana, DimFechaColun.Dia, DimCanal.Descrip_Canal as Canal ,DimSalaColun.Empresa, DimSalaColun.Cadena,  DimProductoColun.DescripcionProducto," 
    query = query +"DimProductoColun.Fabricante_colun, DimProductoColun.Marca_colun, DimProductoColun.Categoria, FactVentasColun.preciounit FROM DimFechaColun INNER JOIN FactVentasColun ON DimFechaColun.ID_Fecha = FactVentasColun.ID_Fecha INNER JOIN DimSalaColun ON " 
    query = query +"FactVentasColun.ID_Sala = DimSalaColun.ID_Sala INNER JOIN DimProductoColun ON FactVentasColun.ID_Producto = DimProductoColun.UPC INNER JOIN DimCanal ON FactVentasColun.ID_Canal = DimCanal.ID_Canal WHERE DimFechaColun.ID_Fecha BETWEEN ? and ?"

    cursor.execute(query, (desde,hasta))
    columns = [column[0] for column in cursor.description]
    with open(f"{destino}{nameFile}.csv",'w', newline='',encoding='utf-8') as csvfile:
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