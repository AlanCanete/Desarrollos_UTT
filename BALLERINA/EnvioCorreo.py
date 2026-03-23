import pyodbc

servermail ='PRODUCCION10'
databasemail ='msdb'
username = 'JMILLA'
password = 'JM8212'
    
profile_name ='Respaldo Notificaciones'
recipients = 'natalia.camus@upthetrade.com '
subject ='Txt Mensual Ballerina Generados Exitosamente'
body ='Estimada Natalia \nYa se encuentran disponibles los archivos  txt de Ballerina con la info al mes Anterior  \n****  Correo generado automáticamente favor no responder  ****\nSaludos'
copy_recipients = 'jose.parra@upthetrade.com;enrique.gonzalez@upthetrade.com;alan.canete@upthetrade.com'

try:
    conection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={servermail};DATABASE={databasemail};UID={username};PWD={password}'
    conn2 = pyodbc.connect(conection_string)
    cursor2 = conn2.cursor()

    procedure ='sp_send_dbmail'
    parametros = (profile_name,recipients,copy_recipients,'',subject,body)

    call_procedure = f"EXEC {procedure} ?,?,?,?,?,?"

    cursor2.execute(call_procedure, parametros)

    conn2.commit()

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    if sqlstate == '28000':
        print("error de autenticacion")
    else:
        print(f"error al ejecutar el procedure: {ex}")
finally:
    if 'cursor2' in locals():
        cursor2.close()
    if 'conn2' in locals():
        conn2.close()