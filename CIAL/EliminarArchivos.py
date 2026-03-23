import paramiko

def UploadFileSftp(rutaOrigen, rutaDestino):
    #credenciales para conexion
    hostname = '200.42.172.228'
    port = 2230
    username = 'sftp.mark'
    password = ':^96f^4o4Mg~qepvO'
    rutasftp = f"/Semanales/{rutaDestino}"
    try:
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.remove(rutasftp)   
        print("eliminado")

        sftp.close()
        transport.close()

    except paramiko.AuthenticationException:
        print("Error de autenticacion. Verifica tus credenciales.")
    except paramiko.SSHException as e:
        print(f"Error de conexion SSH: {e}")
    except FileNotFoundError:
        print(f"Error: El archivo local '{rutaOrigen}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrio un error: {e}")


rutOri='//produccion20/XLSX/CIAL/S Carnes Congeladas.csv'
archivo='S Precios.csv'

UploadFileSftp(rutOri,archivo)