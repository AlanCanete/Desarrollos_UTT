import paramiko

def UploadFileSFTP(rutaOrigen,Archivo):
    hostname = '200.42.172.228'
    port = 2230
    username = 'sftp.mark'
    password = ':^96f^4o4Mg~qepvO'
    rutasftp = f"/Semanales/{Archivo}"
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname,port, username, password)
        sftp_client = ssh_client.open_sftp()
        
        sftp_client.put(rutaOrigen,rutasftp)
        print(f'Subiendo archivo {Archivo} a sftp CIAL')
    except paramiko.AuthenticationException:
        print("Error de autenticacion. Verifiqua tus credenciales.")
    except paramiko.SSHException as e:
        print(f"Error de conexion SSH: {e}")
    except FileNotFoundError:
        print(f"Error: El archivo '{Archivo}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        if 'sftp_client' in locals() and sftp_client:
            sftp_client.close()
        if 'ssh_client' in locals() and ssh_client:
            ssh_client.close()

