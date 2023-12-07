import sys 
import json
import asyncio
import aiohttp
import aiofiles
import time

async def main():
    arg = await check_argument()
    html_content = await get_content()
    await write_content(html_content, "/tmp/web_page.log")

async def check_argument() -> str: 
    if len(sys.argv) != 1:
        print("no argument")
        exit(2)

async def get_content(): 
    with open("urls.json", "r") as file:
        urls = json.load(file)['urls']
        for url in urls:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status != 200:
                            print("bad status code")
                            exit(3)
                        return await response.text()
            except:
                print("cant retrieve url")
                exit(3)

async def write_content(content: str, file: str):
    async with aiofiles.open(file, mode='w') as web_page:
        await web_page.write(content)
    web_page.close()

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    exec_time = end - start
    print(exec_time)
