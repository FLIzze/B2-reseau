import socket
from datetime import datetime
import re

host = "10.1.2.12"
port = 1111
error = ()

logPath = '/var/log/bs_client/bs_client.log'

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host, port))
    except:
        log('ERROR', f'Impossible de se connecter au serveur {host} sur le port {port}')
        exit(2)

    log('INFO', f'Connexion réussie à {host}:{port}.')
    print("+, - et * seulement sont autoriśes, chiffres [-100000, 100000] seulement")
    dataFromClient = input("Saisissez une opération arithmétique: ")

    if checkInput(dataFromClient) == False:
        raise error[0](error[1])
        exit(1)

    s.sendall(dataFromClient.encode('utf-8'))
    log('INFO', f'Message envoyé au serveur {host} : {dataFromClient}.')
    dataFromServer = s.recv(1024)
    print(dataFromServer.decode('utf-8'))
    log('INFO', f"Réponse reçue du serveur {host} : {dataFromServer.decode('utf-8')}.")
    exit(0) 


def checkInput(dataFromClient):
    if type(dataFromClient) != str:
        #raise TypeError("Le message doit etre une string.")
        return False
    else:
        result = re.match("^-?(100000|[0-9]{1,5})(\+|\-|\*)-?(100000|[0-9]{1,5})$", dataFromClient)
        if result == None:
            global error
            error = (ValueError, "Mauvais calcul")
            return False
    return True

def log(hierachy, string):
    global logPath
    global host
    global port
 
    log = open(logPath, 'a')
    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')

    log.write(f"{date} [{hierachy}] {string}\n")
    
    if hierachy == 'ERROR':
        print(f"\033[0;31mERROR Impossible de se connecter au serveur {host} sur le port {port}.\033[0:0m")

connect()
