import asyncio

host = "127.0.0.1"
port = 6969

global CLIENTS
CLIENTS = {}

async def start_server():
    try:
        server = await asyncio.start_server(handle_client, host, port)
    except:
        print(f"couldnt start server on {host}:{port}")
        exit(2)

    async with server:
        await server.serve_forever()
   
async def handle_client(reader, writer):
    client_host = writer.get_extra_info('peername')[0]
    client_port = writer.get_extra_info('peername')[1]

    print(f"new client: {client_host}:{client_port}") 
    writer.write(f"Hello {client_host}:{client_port}".encode('utf-8'))
    await writer.drain()

    while True:
        data = (await reader.read(1024)).decode('utf-8')
        if 'Hello|' in data:
            username = data.split('|')
            username = username[1]
            CLIENTS[writer.get_extra_info('peername')] = reader, writer, username
            await send_all(f"Annonce: <{username}> a rejoint la chatroom", writer)
        elif data != "":
            from_who = CLIENTS[writer.get_extra_info('peername')][2]
            print(f"Message received from {from_who}: {data}")
            await send_all(f"{from_who} a dit : {data}", writer)
        else:
            print(f"{client_host}:{client_port} left")
            client.writer.close()
            break

async def send_all(message: str, writer):
    for client in CLIENTS:
        if client != writer.get_extra_info('peername'):
            client_writer = CLIENTS[(client)][1] 
            client_writer.write((message).encode('utf-8'))
            await client_writer.drain()

async def main():
    await start_server()

if __name__ == "__main__":
    asyncio.run(main())
