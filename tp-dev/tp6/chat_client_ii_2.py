import socket

host = "127.0.0.1"
port = 6969

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = input('input get: ') 

    try:
        s.connect((host, port))
    except:
        print("can't connect to server")
        exit(2)

    s.sendall(data.encode('utf-8'))
    dataFromServer = s.recv(1024)

    print(f"from server: {dataFromServer.decode('utf-8')}")
    exit(0) 

if __name__ == "__main__":
    client()
