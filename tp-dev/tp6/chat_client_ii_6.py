import asyncio
import signal
import aioconsole

host = "127.0.0.1"
port = 6969

class Client:
    def __init__(self, reader, writer):
        self.reader = reader 
        self.writer = writer 

async def connect():
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except:
        print("couldnt connect to server")
        exit(2)
    return reader, writer

async def async_input():
    client.writer.write(f"Hello|{username}".encode('utf-8'))
    await client.writer.drain()
    while True:
        input_client = await aioconsole.ainput()
        client.writer.write(input_client.encode('utf-8'))
        await client.writer.drain()

async def async_receive():
    while True:
        data_from_server = await client.reader.read(1024)
        if data_from_server != b"":
            print(data_from_server.decode())
        else:
            print(f"Le server {host}:{port} vient de fermer... [ctrl + c] pour quitter.")
            await client.writer.wait_closed()

def signal_handler(signal, frame):
    client.writer.close()
    exit(1)

def username_select():
    global username
    username = input("choisis un pseudo: ")

async def main():
    reader, writer = await connect()
    global client
    client = Client(reader, writer)
    signal.signal(signal.SIGINT, signal_handler)
    username_select()
    await asyncio.gather(async_input(), async_receive())

if __name__ == "__main__":
    asyncio.run(main())
