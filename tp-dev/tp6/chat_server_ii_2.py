import asyncio

host = "127.0.0.1"
port = 6969

async def start_server():
    try:
        server = await asyncio.start_server(handle_client, host, port)
    except:
        print(f"couldnt start server on {host}:{port}")
        exit(2)

    async with server:
        await server.serve_forever()
   
async def handle_client(reader, writer):
    print(f"new client: {writer.get_extra_info('peername')[0]}:{writer.get_extra_info(    'peername')[1]}")
    writer.write(f"Hello {writer.get_extra_info('peername')[0]}:{writer.get_extra_info(    'peername')[1]}".encode('utf-8'))
    await writer.drain()

    while True:
        data = await reader.read(1024)
        if data != b"":
            print(f"Message received from {writer.get_extra_info('peername')[0]}:{writer.get_extra_info('peername')[1]}: {data.decode('utf-8')}")
        else:
            print(f"{writer.get_extra_info('peername')[0]}:{writer.get_extra_info('peername')[1]} left")
            client.writer.close()
            break

async def main():
    await start_server()

if __name__ == "__main__":
    asyncio.run(main())
