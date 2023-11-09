import socket
import os
from datetime import datetime
from sys import argv

port = 13337
host = "10.1.2.12"

logPath = '/var/log/bs_server/bs_server.log'

def server():
    arg()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    log('INFO', f'Le serveur tourne sur {host}:{port}')
    s.listen(1)
    
    s.settimeout(60)
    timeout = False

    while timeout == False:
        try:
            conn, addr = s.accept()
            timeout = True
        except socket.timeout:
            log('WARN', 'Aucun client depuis plus de une minute.')
        
    log('INFO', f"Un client {addr[0]} s'est connecté.")

    while True:
        try:
            data = conn.recv(1024)
            data = data.decode('utf-8')
            if not data: break
            log('INFO', f"Le client {addr[0]} a envoyé {data}")
            toClient = compute(data)
            conn.sendall(toClient.encode('utf-8'))
            log('INFO', f"Réponse envoyée au client {addr[0]} : {toClient}")
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

def log(hierachy, string):
    global logPath

    log = open(logPath, 'a')
    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')
    
    log.write(f"{date} [{hierachy}] {string}\n")
    if hierachy == 'WARN':
        print(f"\033[0;33m{date} [{hierachy}] {string}\033[0;0m")
    else:
        print(f"{date} [{hierachy}] {string}")    

    log.close()

def compute(expression):
    return str(eval(expression))

server() 
