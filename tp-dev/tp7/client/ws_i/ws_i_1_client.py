import asyncio
import websockets
from aioconsole import ainput

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            name = await ainput("to server: ")
            await websocket.send(name)
            data = await websocket.recv()
            print(f"{data}")

if __name__ == "__main__":
    asyncio.run(hello())
