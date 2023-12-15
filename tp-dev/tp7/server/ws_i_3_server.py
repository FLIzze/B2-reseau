import asyncio
from websockets.server import serve

port = 8765
host = "localhost"

global CLIENTS
CLIENTS = {}

async def handle_client(websocket):
    async for message in websocket:
        if message.startswith("Hello|"):
            username = message.split("|")
            CLIENTS[websocket] = username[1]
        elif message != "":
            for client in CLIENTS:
                await client.send(f"{CLIENTS[websocket]}: {message}")

async def main():
    async with serve(handle_client, host, port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
