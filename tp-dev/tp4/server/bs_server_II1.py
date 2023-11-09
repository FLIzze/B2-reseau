import socket
from sys import argv

port = 13337
host = "10.1.2.12"

def server():
    arg()
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

def arg():
    if len(argv) == 2:
        if argv[1] == '--help' or argv[1] == '-h':
            print("-h --help  display this text\n-p --port  specify port")
            print("\nExit status:\n1 : port not specify\n2 : missing argument\n3: argument is not a string")
            exit(0)
        else:
            print("missing argument")
            exit(3)
    elif len(argv) == 3:
        if type(argv[2]) != str:
            raise ValueError("argument must be a string")
        else:
            if argv[1] == '--port' or argv[1] == '-p':
                global port
                port = int(argv[2])
                if port < 0 or port > 65535:
                    print("ERROR Le port spécifié n'est pas un port possible (de 0 à 65535)")
                    exit(1)
                elif port >= 0 and port <= 1024:
                    print("ERROR Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.")
                    exit(2)
            else:
                print("missing argument")
                exit(3)


server() 
