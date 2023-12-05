import socket
from datetime import datetime

port = 84
host = "localhost"
logPath = '/var/log/web_server/web_server.log'

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

        try:    
            html_file = open(f"html/{file_name[0]}")
        except:
            html_content = 'file does not exist'
            conn.send(html_content.encode('utf-8'))
            log('INFO', f"Réponse envoyée au client {addr[0]} : {html_content}")
            exit(2)

        html_content = html_file.read()
        http_response = 'HTTP/1.0 200 OK\n\n' + html_content
        conn.send(http_response.encode('utf-8'))
        log('INFO', f"Réponse envoyée au client {addr[0]} : {file_name[0].encode('utf-8')}")
        html_file.close()
        conn.close()
        s.close()

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

server() 
