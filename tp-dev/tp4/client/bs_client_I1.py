import socket

host = "10.1.2.12"
port = 13337

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = "Meooooo !"	
    s.connect((host, port))
    s.sendall(data.encode('utf-8'))
    dataFromServer = s.recv(1024)
    print(f"from server: {dataFromServer.decode('utf-8')}")
    exit(0) 

connect()
