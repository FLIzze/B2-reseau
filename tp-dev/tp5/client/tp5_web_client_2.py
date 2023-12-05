import socket
from datetime import datetime

host = "localhost"
port_input = input('select port: ')
port = int(port_input)

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = input('input get: ') 

    try:
        s.connect((host, port))
    except:
        exit(2)

    s.sendall(data.encode('utf-8'))
    dataFromServer = s.recv(1024)

    print(f"{dataFromServer.decode('utf-8')}")
    exit(0) 

client()

