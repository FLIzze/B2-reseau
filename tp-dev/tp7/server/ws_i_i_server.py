import asyncio
from websockets.server import serve

port = 8765
host = "localhost"

async def echo(websocket):
    async for message in websocket:
        print(message)
        await websocket.send(f"Hello client | Received \"{message}\"")

async def main():
    async with serve(echo, host, port):
        await asyncio.Future()  # run forever

asyncio.run(main())
