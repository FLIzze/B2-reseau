import socket
from datetime import datetime

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
            exit(2)

        html_content = html_file.read()
        http_response = 'HTTP/1.0 200 OK\n\n' + html_content
        conn.send(http_response.encode('utf-8'))
        html_file.close()
        conn.close()
        s.close()

server() 
