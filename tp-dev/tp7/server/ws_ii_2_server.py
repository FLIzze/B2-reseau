import asyncio
from websockets.server import serve
import redis.asyncio as redis

port = 8765
host = "127.0.0.1"

global CLIENTS
CLIENTS = {}

async def handle_client(websocket):
    async for message in websocket:
        if message.startswith("Hello|"):
            global username
            username = message.split("|")
            CLIENTS[websocket] = str(websocket)
            await client.set(str(websocket), username[1])
        elif message != "":
            for client_id in CLIENTS:
                username = await client.get(str(websocket))
                await client_id.send(f"{username.decode()}: {message}")

async def main():
    global client
    client = redis.Redis(host="10.1.1.254", port=6379)
    await client.flushall()
    async with serve(handle_client, host, port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
