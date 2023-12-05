import socket

port = 84
host = "localhost"

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            message = data.decode('utf-8')
            if 'GET /'in message:
                conn.send(('HTTP/1.0 200 OK\n\n<h1>Hello je suis un serveur HTTP</h1>').encode('utf-8'))
                exit(0)
            else:
                exit(1)
        except socket.error:
            print("couldnt retrieve data from client")
            break

    conn.close()
    s.close()

server() 

