import socket

host = "10.1.2.12"
port = 13337

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print(f"Connecté avec succès au serveur {host} sur le port {port}") 
        data = input("Que veux-tu envoyer au serveur : ")
        s.sendall(data.encode('utf-8'))
        dataFromServer = s.recv(1024)
        print(f"from server: {dataFromServer.decode('utf-8')}")
    except:
        print("connexion au serveur impossible")
    exit(0) 

connect()
