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

    CLIENTS[(client_host, client_port)] = reader, writer

    print(f"new client: {client_host}:{client_port}") 
    writer.write(f"Hello {client_host}:{client_port}".encode('utf-8'))
    await writer.drain()

    while True:
        data = await reader.read(1024)
        if data != b"":
            print(f"Message received from {client_host}:{client_port}: {data.decode('utf-8')}")
            for client in CLIENTS:
                if client != writer.get_extra_info('peername'):
                    client_writer = CLIENTS[(client)][1] 
                    client_writer.write((f"{client_host}:{client_port} a dit : {data.decode('utf-8')}").encode('utf-8'))
                    await client_writer.drain()
        else:
            print(f"{client_host}:{client_port} left")
            client.writer.close()
            break

async def main():
    await start_server()

if __name__ == "__main__":
    asyncio.run(main())
