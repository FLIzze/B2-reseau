import socket
from datetime import datetime

port = 81
host = "localhost"
logPath = '/var/log/web_server/web_server.log'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()

def server():
    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            message = data.decode('utf-8')
            log('INFO', f"Le client {addr[0]} a envoyé {data}")
        except socket.error:
            exit(1)
        file_name = 'this html file does not exist'
                
        if 'GET /' in message:
            split_msg = message.split('/')
            file_name_splited = split_msg[1]
            file_name = file_name_splited.split(' ')
        else:
            conn.send(b'need to GET /')

        http_response = b''

        if '.png' in message or '.jpg' in message:
            try:    
                with open(f'img/{file_name[0]}', 'rb') as img:
                    lines = img.readlines()
                img.close()
                html_content = lines
            except:
                html_content = 'file does not exist'.encode('utf-8')
            log('INFO', f"Réponse envoyée au client {addr[0]} : {html_content}")

            for line in lines:
                http_response += line
        #conn.send(lines.decode('utf-8'))
            log('INFO', f"Réponse envoyée au client {addr[0]} : {file_name[0].encode('utf-8')}")
            img.close()
            send_data(http_response)
        else:
            try:    
                html_content = open(f"html/{file_name[0]}")
            except:
                html_content = 'file does not exist'
                send_data(html_content.encode('utf-8'))
                exit(2)

            http_response = 'HTTP/1.0 200 OK\n\n' + html_content.read()
            log('INFO', f"Réponse envoyée au client {addr[0]} : {html_content}")
            send_data(http_response.encode('utf-8'))
        conn.close()
        s.close()
        exit(1)

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

def send_data(http_response: bytes):
    msg_len = len(http_response)
    header = msg_len.to_bytes(4, byteorder='big')
    tail = 0
    tail = tail.to_bytes(1, byteorder='big')
    payload = header + http_response + tail
    conn.sendall(payload)

server() 
