import socket

port = 13337
host = "10.1.2.12"

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            print(f"from client: {data.decode('utf-8')}")
            conn.sendall(b"Hi mate !")
        except socket.error:
            print("couldnt retrieve data from client")
            break
    conn.close()

server() 
