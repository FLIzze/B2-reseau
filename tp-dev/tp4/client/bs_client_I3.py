import socket
import re

host = "10.1.2.12"
port = 1111
error = ()

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host, port))
    except:
        print("connexion au serveur impossible")
        exit(1)

    print(f"Connecté avec succès au serveur {host} sur le port {port}") 
    dataFromClient = input("Que veux-tu envoyer au serveur : ")

    if checkInput(dataFromClient) == False:
        raise error[0](error[1])
        exit(1)

    s.sendall(dataFromClient.encode('utf-8'))
    dataFromServer = s.recv(1024)
    print(f"from server: {dataFromServer.decode('utf-8')}")
    exit(0) 


def checkInput(dataFromClient):
	global error
	if type(dataFromClient) != str:
        #raise TypeError("Le message doit etre une string.")
		error = (TypeError, "Le message doit etre une string.")
		return False
	else:
        	result = re.match("^.*(waf|meo).*$", dataFromClient)
        if result == None:
            #raise ValueError("Le message doit contenir 'waf' ou 'meo'")
            error = (ValueError, "Le message doit contenir 'waf' ou 'meo'")
            return False
    return True

connect()
