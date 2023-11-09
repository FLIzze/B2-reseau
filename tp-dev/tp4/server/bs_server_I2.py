import socket

port = 13337
host = "10.1.2.12"

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    print(f"Un client vient de se co et son IP c'est {addr[0]}.")
    while True:
        try:
            data = conn.recv(1024)
            data = data.decode('utf-8')
            if not data: break
            print(f"from client: {data}")
            if "meo" in data:
                toClient = "Meo à toi confrère."
            elif 'waf' in data:
                toClient = 'ptdr t ki'
            else:
                toClient = "Mes respects humble humain."
            conn.sendall(toClient.encode('utf-8'))
        except socket.error:
            print("couldnt retrieve data from client")
            break
    conn.close()

server() 
