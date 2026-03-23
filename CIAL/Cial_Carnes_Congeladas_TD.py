import pyodbc
import csv
import datetime
import paramiko

Server = 'clientes5'
database = 'CLIENTES_CIAL'
user = 'acanete'
password = 'Canete2025@utt'
conection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={Server};DATABASE={database};UID={user};PWD={password}'
destino = '//produccion20/XLSX/CIAL/'
nameFile = 'S Carnes Congeladas '

def ObtieneAgnoSemana():
    today = datetime.date.today()
    agno_iso, semana_iso, dia_iso = today.isocalendar()
    if semana_iso == 1:
        agno = agno_iso - 1
        semana = 12
    else:
        agno = agno_iso
        semana = semana_iso - 1

    return agno,semana

def UploadFileSftp(rutaOrigen, rutaDestino):
    #credenciales para conexion
    hostname = '200.42.172.228'
    port = 2230
    username = 'sftp.mark'
    password = ':^96f^4o4Mg~qepvO'
    rutasftp = f"/Semanales/Carnes congeladas/{rutaDestino}"
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname,port,username=username,password=password)
        sftp_client = ssh_client.open_sftp()
        sftp_client.put(rutaOrigen,rutasftp)
        print("¡Archivo cargado exitosamente!")    

    except paramiko.AuthenticationException:
        print("Error de autenticacion. Verifica tus credenciales.")
    except paramiko.SSHException as e:
        print(f"Error de conexion SSH: {e}")
    except FileNotFoundError:
        print(f"Error: El archivo local '{rutaOrigen}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        if 'sftp_client' in locals() and sftp_client:
            sftp_client.close()
        if 'ssh_client' in locals() and ssh_client:
            ssh_client.close()

try:
    agno_f, semana_f = ObtieneAgnoSemana()
    aux = str(agno_f)
    agnoCut = aux[2:4]
    conn = pyodbc.connect(conection_string)
    cursor = conn.cursor()

    query = "SELECT * FROM [CLIENTES_CIAL].[dbo].[TBL_CarnesCongeladas_TB] WITH(NOLOCK)"

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]

    with open(f"{destino}{nameFile}- TD.csv",'w',newline='',encoding='utf-8')as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(columns)
        for row in cursor.fetchall():
            writer.writerow(row)

    archivo=f"{nameFile}- TD.csv"
    rutaOrigen = f"{destino}{archivo}"
    UploadFileSftp(rutaOrigen,archivo)
    
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error al conectar a SQL Server: {sqlstate}")
    exit()
except Exception as e:
    print(f"Ocurrio un error: {e}")
finally:
    cursor.close()
    conn.close()