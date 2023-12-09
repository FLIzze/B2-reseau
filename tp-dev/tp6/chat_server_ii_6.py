import asyncio
import signal

host = "127.0.0.1"
port = 6969

global CLIENTS
CLIENTS = {}

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

    print(f"new client: {client_host}:{client_port}") 
    writer.write(f"Hello {client_host}:{client_port}".encode('utf-8'))
    await writer.drain()

    while True:
        try:
            data = (await reader.read(1024)).decode('utf-8')
        except:
            print(f"{client_host}:{client_port} déconnexion")
            break

        if 'Hello|' in data:
            username = data.split('|')
            username = username[1]
            CLIENTS[client_info] = reader, writer, username
            await send_all(f"Annonce : <{username}> a rejoint la chatroom", writer)
            print(f"<{username}> pseudo de {client_host}:{client_port}")
        elif data != "":
            from_who = CLIENTS[client_info][2]
            print(f"Message received from <{from_who}>: {data}")
            await send_all(f"<{from_who}>: {data}", writer)
        else:
            from_who = CLIENTS[client_info][2]
            print(f"{client_host}:{client_port} ({from_who}) left")
            await send_all(f"Annonce : <{from_who}> a quitté la chatroom", writer)
            CLIENTS.pop(client_info)
            break

async def send_all(message: str, writer):
    for client in CLIENTS:
        if client != writer.get_extra_info('peername'):
            client_writer = CLIENTS[(client)][1] 
            client_writer.write((message).encode('utf-8'))
            await client_writer.drain()

def signal_handler(signal, frame):
    server.close()
    print("fermeture du serveur...")
    exit(1)

async def main():
    signal.signal(signal.SIGINT, signal_handler)
    await start_server()

if __name__ == "__main__":
    asyncio.run(main())
