import socket
from datetime import datetime

host = "localhost"
port_input = input('select port: ')
port = int(port_input)
logPath = '/var/log/web_server/web_client.log'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chunks = []

def client():
    global chunks
    data = input('input get: ') 

    try:
        s.connect((host, port))
        log('INFO', f'Connexion réussie à {host}:{port}.')
    except:
        log('ERROR', f'Impossible de se connecter au serveur {host} sur le port {port}')
        exit(2)

    s.sendall(data.encode('utf-8'))
    #dataFromServer = s.recv(1024)
    header = s.recv(4)
    if not header: exit(3)
    msg_len = int.from_bytes(header[0:4], byteorder='big')

    print(f"Lecture des {msg_len} prochains octets")

    bytes_received = 0
    while bytes_received < msg_len:
        chunk = s.recv(min(msg_len - bytes_received, 1024))
        if not chunk:
            raise RunTimeError('Invalid chunk received bro')

        chunks.append(chunk)
        bytes_received += len(chunk)

    tail = s.recv(1)
    if int.from_bytes(tail, 'big') == 0:
        print('Received end of message')

    if '.png' in data or '.jpg' in data: 
        print("test")
        download_image(chunks)
    else:
        for chunk in chunks:
            print(chunk.decode('utf-8'))

    #if dataFromServer.decode('utf-8') == 'file does not exist':
        #log('WARN', f'Bad request: {data}')
    #else:
        #log('INFO', f'{data}')

    #print(f"{dataFromServer}")
    s.close()
    exit(0) 

def log(hierachy, string):
    global logPath
    global host
    global port
 
    log = open(logPath, 'a')
    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')

    log.write(f"{date} [{hierachy}] {string}\n")
    
    if hierachy == 'ERROR':
        print(f"\033[0;31mERROR Impossible de se connecter au serveur {host} sur le port {port}.\033[0:0m")
    elif hierachy == 'WARN':
        print(f"\033[0;33m{date} [{hierachy}] {string}\033[0;0m")

def download_image(bytes_iamge):
    with open("./img_test.jpg", "wb") as binary_image:
        for chunk in chunks:
            binary_image.write(chunk)
        binary_image.close()
        
client()

