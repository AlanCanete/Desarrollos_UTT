import pyodbc

servermail = 'PRODUCCION18'
databasemail = 'msdb'
usermail = 'JMILLA'
passmail = 'JM8212'

profile_name ='Respaldo Notificaciones'
recipients = 'fernanda.prato@upthetrade.com'
subject ='NOTIFICACION - PLANOS CIAL'
body = f"Buenos Dias.\n Se informa que ya se encuentra disponible en Produccion y servidor SFTP los Planos de CIAL. \n\n\nSaludos\nUpthetrade"
copy_recipients = 'alan.canete@upthetrade.com;jose.parra@utt.cl'

try:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={servermail};DATABASE={databasemail};UID={usermail};PWD={passmail}'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    procedure = 'sp_send_dbmail'
    parametros = (profile_name, recipients, copy_recipients,'',subject,body)
    call_procedure = f"EXEC {procedure} ?,?,?,?,?,?"
    cursor.execute(call_procedure, parametros)
    conn.commit()
except Exception as ex:
    print(f"Ocurrio un error: {ex}")
except pyodbc.Error as e:
    sqlstate = e.args[0]
    if sqlstate == '28000':
        print("Error de autenticacion")
    else:
        print(f"Error al ejecutar el procedure: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()