import asyncio
import signal
from datetime import datetime
import random
from chat_args_and_config import *

class Client:
    all_clients = {}
    def __init__(self, host, port, username, color, uid, writer):
        self.host = host
        self.port = port
        self.username = username
        self.color = color
        self.uid = uid
        self.writer = writer
        Client.all_clients[(self.host, self.port)] = username, color, uid, writer

async def start_server():
    try:
        global server
        server = await asyncio.start_server(handle_client, host, port)
    except:
        print(f"couldnt start server on {host}:{port}")
        exit(2)

    async with server:
        await server.serve_forever()
   
async def handle_client(reader, writer):
    client_info = writer.get_extra_info('peername')
    client_host = client_info[0]
    client_port = client_info[1] 

    while True:
        try:
            data = (await reader.read(1024)).decode('utf-8')
        except:
            print(f"{client_host}:{client_port} déconnexion")
            break

        time = datetime.now()
        time_formated = time.strftime('%H:%M')

        if data.startswith('Hello|'): 
            username = data.split('|')
            username = username[1]

            color1 = random.randint(0, 256)
            color2 = random.randint(0, 256)
            color3  = random.randint(0, 256)

            global client
            client = Client(client_host, client_port, username, (color1, color2, color3), client_port, writer)
            await send_info(f"[{time_formated}] Annonce:\033[38;2;{color1};{color2};{color3}m {username} \033[0ma rejoint la chatroom", writer)
        elif data != "":
            for client in Client.all_clients:
                if Client.all_clients[client][2] == client_port:
                    cli = Client.all_clients[client]
                    await send_info(f"[{time_formated}]\033[38;2;{cli[1][0]};{cli[1][1]};{cli[1][2]}m {cli[0]}\033[0m: {data}", cli[3])
        else:
            for client in Client.all_clients:
                if Client.all_clients[client][2] == client_port:
                    cli = Client.all_clients[client]
                    await send_info(f"[{time_formated}] Annonce:\033[38;2;{cli[1][0]};{cli[1][1]};{cli[1][2]}m {cli[0]}\033[0m a quitté la chatroom", cli[3])
            del Client.all_clients[(client_host, client_port)]
            break

async def send_to_all(message: str, writer):
    for client in Client.all_clients:
        if client != writer.get_extra_info('peername'):
            client_writer = Client.all_clients[(client)][3] 
            client_writer.write(message.encode('utf-8'))
            await client_writer.drain()

async def send_info(message: str, writer):
    await send_to_all(message, writer)
    print(message)

def signal_handler(signal, frame):
    server.close()
    print(f"fermeture du serveur... {host}:{port}")
    exit(1)

async def main():
    global host, port
    host, port = ip_config()
    if host == 0 and port == 0:
        host, port = args()
    print(f"ouverture du serveur {host}:{port}")
    signal.signal(signal.SIGINT, signal_handler)
    await start_server()

if __name__ == "__main__":
    asyncio.run(main())
